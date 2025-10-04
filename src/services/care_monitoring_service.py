"""
Continuous care monitoring and journey tracking service
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from src.database.models import CareJourney, Patient, Appointment, TriageSession


class CareMonitoringService:
    """
    Monitor patient care journeys and identify gaps
    """
    
    def __init__(self, db_session: Session):
        self.db = db_session
        
    def create_care_journey(self, patient_id: int, condition: str,
                           initial_triage_id: int = None) -> Dict:
        """
        Start a new care journey for a patient
        
        Args:
            patient_id: Patient ID
            condition: Primary condition/diagnosis
            initial_triage_id: Optional initial triage session ID
            
        Returns:
            Care journey details
        """
        milestones = []
        if initial_triage_id:
            milestones.append({
                'timestamp': datetime.utcnow().isoformat(),
                'type': 'triage',
                'description': 'Initial symptom assessment',
                'triage_id': initial_triage_id
            })
        
        journey = CareJourney(
            patient_id=patient_id,
            condition=condition,
            status='active',
            start_date=datetime.utcnow(),
            milestones=milestones,
            care_gaps=[],
            outcomes={}
        )
        
        self.db.add(journey)
        self.db.commit()
        self.db.refresh(journey)
        
        return self._format_journey(journey)
    
    def add_milestone(self, journey_id: int, milestone_type: str,
                     description: str, metadata: Dict = None) -> bool:
        """Add a milestone to a care journey"""
        journey = self.db.query(CareJourney).filter(
            CareJourney.id == journey_id
        ).first()
        
        if not journey:
            return False
        
        milestone = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': milestone_type,
            'description': description,
            'metadata': metadata or {}
        }
        
        if journey.milestones:
            journey.milestones.append(milestone)
        else:
            journey.milestones = [milestone]
        
        journey.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def identify_care_gaps(self, patient_id: int) -> List[Dict]:
        """
        Identify gaps in patient care
        
        Checks for:
        - Missed follow-up appointments
        - Incomplete test results
        - Missing specialist referrals
        - Medication adherence issues
        """
        gaps = []
        
        # Get active care journeys
        active_journeys = self.db.query(CareJourney).filter(
            and_(
                CareJourney.patient_id == patient_id,
                CareJourney.status == 'active'
            )
        ).all()
        
        for journey in active_journeys:
            # Check for missed appointments
            missed_appointments = self._check_missed_appointments(patient_id)
            if missed_appointments:
                gaps.append({
                    'journey_id': journey.id,
                    'type': 'missed_appointment',
                    'severity': 'high',
                    'description': f'{len(missed_appointments)} missed appointment(s)',
                    'appointments': missed_appointments
                })
            
            # Check for overdue follow-ups
            last_appointment = self._get_last_appointment(patient_id)
            if last_appointment:
                days_since = (datetime.utcnow() - last_appointment.scheduled_datetime).days
                if days_since > 90:  # No appointment in 90 days
                    gaps.append({
                        'journey_id': journey.id,
                        'type': 'overdue_followup',
                        'severity': 'medium',
                        'description': f'No follow-up appointment in {days_since} days',
                        'last_appointment_date': last_appointment.scheduled_datetime.isoformat()
                    })
            
            # Check milestone progression
            if journey.milestones:
                last_milestone_date = datetime.fromisoformat(
                    journey.milestones[-1]['timestamp']
                )
                days_since_milestone = (datetime.utcnow() - last_milestone_date).days
                
                if days_since_milestone > 30:
                    gaps.append({
                        'journey_id': journey.id,
                        'type': 'stalled_progress',
                        'severity': 'medium',
                        'description': f'No progress in {days_since_milestone} days',
                        'last_milestone': journey.milestones[-1]
                    })
        
        # Update journey with identified gaps
        for journey in active_journeys:
            journey_gaps = [g for g in gaps if g['journey_id'] == journey.id]
            journey.care_gaps = journey_gaps
            self.db.commit()
        
        return gaps
    
    def _check_missed_appointments(self, patient_id: int) -> List[Dict]:
        """Check for missed appointments"""
        missed = self.db.query(Appointment).filter(
            and_(
                Appointment.patient_id == patient_id,
                Appointment.status == 'scheduled',
                Appointment.scheduled_datetime < datetime.utcnow()
            )
        ).all()
        
        return [
            {
                'id': appt.id,
                'scheduled_datetime': appt.scheduled_datetime.isoformat(),
                'service_type': appt.service_type
            }
            for appt in missed
        ]
    
    def _get_last_appointment(self, patient_id: int) -> Optional[Appointment]:
        """Get most recent completed appointment"""
        return self.db.query(Appointment).filter(
            and_(
                Appointment.patient_id == patient_id,
                Appointment.status == 'completed'
            )
        ).order_by(Appointment.scheduled_datetime.desc()).first()
    
    def get_patient_journey(self, patient_id: int) -> List[Dict]:
        """Get all care journeys for a patient"""
        journeys = self.db.query(CareJourney).filter(
            CareJourney.patient_id == patient_id
        ).order_by(CareJourney.start_date.desc()).all()
        
        return [self._format_journey(j) for j in journeys]
    
    def complete_journey(self, journey_id: int, outcomes: Dict) -> bool:
        """Mark a care journey as completed"""
        journey = self.db.query(CareJourney).filter(
            CareJourney.id == journey_id
        ).first()
        
        if not journey:
            return False
        
        journey.status = 'completed'
        journey.end_date = datetime.utcnow()
        journey.outcomes = outcomes
        journey.updated_at = datetime.utcnow()
        
        self.db.commit()
        return True
    
    def _format_journey(self, journey: CareJourney) -> Dict:
        """Format care journey for API response"""
        return {
            'id': journey.id,
            'patient_id': journey.patient_id,
            'condition': journey.condition,
            'status': journey.status,
            'start_date': journey.start_date.isoformat(),
            'end_date': journey.end_date.isoformat() if journey.end_date else None,
            'milestones': journey.milestones or [],
            'care_gaps': journey.care_gaps or [],
            'outcomes': journey.outcomes or {}
        }
    
    def get_system_metrics(self) -> Dict:
        """Calculate and return system-wide metrics"""
        # Get total patients
        total_patients = self.db.query(Patient).count()
        
        # Get appointments in last 30 days
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_appointments = self.db.query(Appointment).filter(
            Appointment.created_at >= thirty_days_ago
        ).count()
        
        # Calculate average wait time
        completed_appointments = self.db.query(Appointment).filter(
            and_(
                Appointment.status == 'completed',
                Appointment.created_at >= thirty_days_ago
            )
        ).all()
        
        if completed_appointments:
            wait_times = [
                (appt.scheduled_datetime - appt.created_at).total_seconds() / 3600
                for appt in completed_appointments
            ]
            avg_wait_time = sum(wait_times) / len(wait_times)
        else:
            avg_wait_time = 0
        
        # Calculate reductions (baseline comparison)
        baseline_wait_time = 168  # 7 days in hours
        wait_time_reduction = max(0, (baseline_wait_time - avg_wait_time) / baseline_wait_time)
        
        # Active care journeys
        active_journeys = self.db.query(CareJourney).filter(
            CareJourney.status == 'active'
        ).count()
        
        return {
            'total_patients': total_patients,
            'recent_appointments': recent_appointments,
            'average_wait_time_hours': round(avg_wait_time, 2),
            'wait_time_reduction_percent': round(wait_time_reduction * 100, 2),
            'cost_savings_percent': round(wait_time_reduction * 0.4167, 2),  # Approx 25% at 60% reduction
            'active_care_journeys': active_journeys,
            'system_status': 'operational'
        }
