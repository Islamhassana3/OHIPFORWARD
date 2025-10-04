"""
Transportation service integration (Uber Health)
"""
import os
from datetime import datetime, timedelta
from typing import Dict, Optional
from sqlalchemy.orm import Session

from src.database.models import Transportation, Appointment


class TransportationService:
    """
    Integration with Uber Health API for patient transportation
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.api_key = os.getenv('UBER_HEALTH_API_KEY')
        self.enabled = os.getenv('ENABLE_UBER_HEALTH', 'true').lower() == 'true'
        
    def book_ride(self, appointment_id: int, pickup_location: Dict,
                 dropoff_location: Dict = None, scheduled_time: datetime = None) -> Dict:
        """
        Book transportation for an appointment
        
        Args:
            appointment_id: Appointment ID
            pickup_location: Pickup address and coordinates
            dropoff_location: Dropoff address (defaults to appointment location)
            scheduled_time: Scheduled pickup time (defaults to 30 min before appointment)
            
        Returns:
            Transportation booking details
        """
        # Get appointment details
        appointment = self.db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()
        
        if not appointment:
            return {
                'success': False,
                'error': 'Appointment not found'
            }
        
        # Set defaults
        if not dropoff_location:
            dropoff_location = {
                'address': appointment.location
            }
        
        if not scheduled_time:
            # Schedule pickup 30 minutes before appointment
            scheduled_time = appointment.scheduled_datetime - timedelta(minutes=30)
        
        # Create transportation record
        if self.enabled:
            # In production, this would call the actual Uber Health API
            ride_result = self._book_uber_health_ride(
                pickup_location,
                dropoff_location,
                scheduled_time
            )
        else:
            # Mock response for development
            ride_result = {
                'ride_id': f'mock-ride-{appointment_id}',
                'status': 'confirmed',
                'estimated_cost': 15.50,
                'driver_name': 'Mock Driver',
                'vehicle_info': 'Toyota Camry - ABC 123'
            }
        
        # Save transportation record
        transportation = Transportation(
            appointment_id=appointment_id,
            ride_id=ride_result['ride_id'],
            pickup_location=pickup_location.get('address'),
            dropoff_location=dropoff_location.get('address'),
            scheduled_time=scheduled_time,
            status=ride_result['status'],
            cost=ride_result.get('estimated_cost'),
            driver_name=ride_result.get('driver_name'),
            vehicle_info=ride_result.get('vehicle_info')
        )
        
        self.db.add(transportation)
        self.db.commit()
        self.db.refresh(transportation)
        
        return {
            'success': True,
            'rideId': transportation.ride_id,
            'status': transportation.status,
            'scheduledTime': scheduled_time.isoformat(),
            'pickupLocation': pickup_location.get('address'),
            'dropoffLocation': dropoff_location.get('address'),
            'estimatedCost': transportation.cost,
            'driver': {
                'name': transportation.driver_name,
                'vehicle': transportation.vehicle_info
            }
        }
    
    def _book_uber_health_ride(self, pickup: Dict, dropoff: Dict,
                              scheduled_time: datetime) -> Dict:
        """
        Call Uber Health API to book a ride
        
        In production, this would make actual API calls to Uber Health.
        For now, returns mock data.
        """
        # Mock implementation
        # In production, use:
        # import requests
        # response = requests.post(
        #     'https://api.uber.com/v1/health/requests',
        #     headers={'Authorization': f'Bearer {self.api_key}'},
        #     json={...}
        # )
        
        return {
            'ride_id': f'uber-{datetime.now().timestamp()}',
            'status': 'confirmed',
            'estimated_cost': 15.50,
            'driver_name': 'John Smith',
            'driver_phone': '416-555-0199',
            'vehicle_info': 'Toyota Camry - ABC 123'
        }
    
    def get_ride_status(self, ride_id: str) -> Optional[Dict]:
        """Get current status of a ride"""
        transportation = self.db.query(Transportation).filter(
            Transportation.ride_id == ride_id
        ).first()
        
        if not transportation:
            return None
        
        return {
            'rideId': transportation.ride_id,
            'status': transportation.status,
            'scheduledTime': transportation.scheduled_time.isoformat() if transportation.scheduled_time else None,
            'pickupTime': transportation.pickup_time.isoformat() if transportation.pickup_time else None,
            'dropoffTime': transportation.dropoff_time.isoformat() if transportation.dropoff_time else None,
            'driver': {
                'name': transportation.driver_name,
                'phone': transportation.driver_phone,
                'vehicle': transportation.vehicle_info
            }
        }
    
    def cancel_ride(self, ride_id: str) -> bool:
        """Cancel a scheduled ride"""
        transportation = self.db.query(Transportation).filter(
            Transportation.ride_id == ride_id
        ).first()
        
        if transportation and transportation.status in ['pending', 'confirmed']:
            transportation.status = 'cancelled'
            self.db.commit()
            return True
        
        return False
    
    def update_ride_status(self, ride_id: str, status: str,
                          pickup_time: datetime = None,
                          dropoff_time: datetime = None) -> bool:
        """Update ride status (called by webhook or polling)"""
        transportation = self.db.query(Transportation).filter(
            Transportation.ride_id == ride_id
        ).first()
        
        if not transportation:
            return False
        
        transportation.status = status
        if pickup_time:
            transportation.pickup_time = pickup_time
        if dropoff_time:
            transportation.dropoff_time = dropoff_time
        
        self.db.commit()
        return True
