"""
Integration test for complete patient care journey
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base, Patient
from src.ai.triage_engine import SymptomTriageEngine
from src.services.appointment_service import AppointmentService
from src.services.care_monitoring_service import CareMonitoringService


@pytest.fixture
def db_session():
    """Create a test database session"""
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def test_patient(db_session):
    """Create a test patient"""
    patient = Patient(
        ohip_number='1234567890AB',
        first_name='Test',
        last_name='Patient',
        date_of_birth=datetime(1980, 1, 1),
        phone='416-555-0100',
        email='test@example.com'
    )
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    return patient


def test_complete_patient_journey(db_session, test_patient):
    """
    Test a complete patient journey from triage to care monitoring
    """
    # Step 1: Triage symptoms
    triage_engine = SymptomTriageEngine()
    assessment = triage_engine.assess_symptoms(
        symptoms=['fever', 'cough'],
        duration='2 days',
        severity='moderate'
    )
    
    assert assessment['urgency'] in ['routine', 'urgent']
    assert assessment['confidence'] > 0.5
    assert 'recommendedAction' in assessment
    assert len(assessment['nextSteps']) > 0
    
    # Step 2: Create care journey
    care_service = CareMonitoringService(db_session)
    journey_result = care_service.create_care_journey(
        patient_id=test_patient.id,
        condition='Upper Respiratory Infection'
    )
    
    assert journey_result['status'] == 'active'
    assert journey_result['patient_id'] == test_patient.id
    
    # Step 3: Add milestone
    success = care_service.add_milestone(
        journey_id=journey_result['id'],
        milestone_type='triage',
        description='Initial symptom assessment completed'
    )
    
    assert success is True
    
    # Step 4: Get patient journey
    journeys = care_service.get_patient_journey(test_patient.id)
    assert len(journeys) > 0
    assert journeys[0]['condition'] == 'Upper Respiratory Infection'


def test_triage_to_appointment_flow():
    """Test the flow from triage to appointment"""
    triage_engine = SymptomTriageEngine()
    
    # Test urgent case
    assessment = triage_engine.assess_symptoms(
        symptoms=['chest pain', 'difficulty breathing'],
        severity='severe'
    )
    
    assert assessment['urgency'] == 'critical'
    assert '911' in assessment['recommendedAction']
    
    # Test routine case
    assessment = triage_engine.assess_symptoms(
        symptoms=['mild headache', 'fatigue'],
        severity='mild'
    )
    
    assert assessment['urgency'] == 'routine'
    assert 'primary care' in assessment['recommendedAction'].lower()
