"""
Automated appointment scheduling service
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Appointment, Provider, ProviderAvailability, Patient


class AppointmentService:
    """
    Smart scheduling service that optimizes appointment allocation
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def schedule_appointment(self, patient_id: int, service_type: str,
                           urgency: str, preferences: Dict = None) -> Dict:
        """
        Schedule an appointment based on urgency and preferences
        
        Args:
            patient_id: Patient ID
            service_type: Type of service needed
            urgency: Urgency level (critical, urgent, routine)
            preferences: Optional preferences (specialty, location, provider)
            
        Returns:
            Appointment details
        """
        preferences = preferences or {}
        
        # Find suitable providers
        providers = self._find_suitable_providers(
            service_type=service_type,
            specialty=preferences.get('specialty'),
            location=preferences.get('location'),
            max_wait_time=self._get_max_wait_time(urgency)
        )
        
        if not providers:
            return {
                'success': False,
                'error': 'No available providers found matching criteria'
            }
        
        # Find next available slot
        for provider in providers:
            slot = self._find_next_available_slot(
                provider.id,
                urgency,
                preferences.get('preferred_time')
            )
            
            if slot:
                # Create appointment
                appointment = self._create_appointment(
                    patient_id=patient_id,
                    provider_id=provider.id,
                    service_type=service_type,
                    scheduled_datetime=slot,
                    urgency=urgency,
                    location=provider.address
                )
                
                return {
                    'success': True,
                    'appointmentId': appointment.id,
                    'provider': {
                        'id': provider.id,
                        'name': provider.name,
                        'specialty': provider.specialty,
                        'rating': provider.rating,
                        'phone': provider.phone
                    },
                    'dateTime': slot.isoformat(),
                    'location': provider.address,
                    'serviceType': service_type,
                    'urgency': urgency
                }
        
        return {
            'success': False,
            'error': 'No available appointment slots found'
        }
    
    def _find_suitable_providers(self, service_type: str, specialty: str = None,
                                location: str = None, max_wait_time: float = None) -> List:
        """Find providers matching criteria"""
        query = self.db.query(Provider).filter(
            Provider.accepts_new_patients == True
        )
        
        # Filter by specialty if provided
        if specialty:
            query = query.filter(Provider.specialty == specialty)
        
        # Filter by wait time
        if max_wait_time:
            query = query.filter(Provider.average_wait_time_days <= max_wait_time)
        
        # Order by rating and wait time
        providers = query.order_by(
            Provider.rating.desc(),
            Provider.average_wait_time_days.asc()
        ).all()
        
        # TODO: Add location-based filtering with distance calculation
        
        return providers
    
    def _find_next_available_slot(self, provider_id: int, urgency: str,
                                 preferred_time: str = None) -> Optional[datetime]:
        """Find next available time slot for a provider"""
        # Get provider availability
        availability = self.db.query(ProviderAvailability).filter(
            and_(
                ProviderAvailability.provider_id == provider_id,
                ProviderAvailability.is_available == True
            )
        ).all()
        
        if not availability:
            return None
        
        # Determine search window based on urgency
        search_days = self._get_search_window_days(urgency)
        start_date = datetime.now()
        end_date = start_date + timedelta(days=search_days)
        
        # Get existing appointments
        existing_appointments = self.db.query(Appointment).filter(
            and_(
                Appointment.provider_id == provider_id,
                Appointment.scheduled_datetime >= start_date,
                Appointment.scheduled_datetime <= end_date,
                Appointment.status.in_(['scheduled', 'confirmed'])
            )
        ).all()
        
        # Convert to set of occupied time slots
        occupied_slots = {
            appt.scheduled_datetime.replace(minute=0, second=0, microsecond=0)
            for appt in existing_appointments
        }
        
        # Find first available slot
        current_date = start_date
        while current_date <= end_date:
            day_of_week = current_date.weekday()
            
            # Check if provider is available on this day
            day_availability = [
                avail for avail in availability
                if avail.day_of_week == day_of_week
            ]
            
            if day_availability:
                avail = day_availability[0]
                # Parse time slots (9 AM to 5 PM in 30-min increments)
                start_hour = int(avail.start_time.split(':')[0])
                end_hour = int(avail.end_time.split(':')[0])
                
                for hour in range(start_hour, end_hour):
                    for minute in [0, 30]:
                        slot_time = current_date.replace(
                            hour=hour, minute=minute, second=0, microsecond=0
                        )
                        
                        # Check if slot is in the future and not occupied
                        if slot_time > datetime.now() and slot_time not in occupied_slots:
                            return slot_time
            
            # Move to next day
            current_date += timedelta(days=1)
        
        return None
    
    def _create_appointment(self, patient_id: int, provider_id: int,
                          service_type: str, scheduled_datetime: datetime,
                          urgency: str, location: str) -> Appointment:
        """Create a new appointment"""
        appointment = Appointment(
            patient_id=patient_id,
            provider_id=provider_id,
            service_type=service_type,
            scheduled_datetime=scheduled_datetime,
            duration_minutes=30,
            status='scheduled',
            urgency=urgency,
            location=location
        )
        
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        
        return appointment
    
    def _get_max_wait_time(self, urgency: str) -> float:
        """Get maximum acceptable wait time in days based on urgency"""
        wait_times = {
            'critical': 0.5,  # Within 12 hours
            'urgent': 2,      # Within 2 days
            'routine': 7,     # Within 1 week
            'non-urgent': 14  # Within 2 weeks
        }
        return wait_times.get(urgency, 7)
    
    def _get_search_window_days(self, urgency: str) -> int:
        """Get number of days to search for appointments"""
        windows = {
            'critical': 1,
            'urgent': 3,
            'routine': 14,
            'non-urgent': 30
        }
        return windows.get(urgency, 14)
    
    def get_appointment(self, appointment_id: int) -> Optional[Dict]:
        """Get appointment details"""
        appointment = self.db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()
        
        if not appointment:
            return None
        
        return {
            'id': appointment.id,
            'patient_id': appointment.patient_id,
            'provider': {
                'id': appointment.provider.id,
                'name': appointment.provider.name,
                'specialty': appointment.provider.specialty
            },
            'scheduled_datetime': appointment.scheduled_datetime.isoformat(),
            'service_type': appointment.service_type,
            'status': appointment.status,
            'location': appointment.location
        }
    
    def cancel_appointment(self, appointment_id: int) -> bool:
        """Cancel an appointment"""
        appointment = self.db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()
        
        if appointment:
            appointment.status = 'cancelled'
            self.db.commit()
            return True
        
        return False
