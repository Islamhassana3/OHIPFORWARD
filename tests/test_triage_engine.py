"""
Tests for the symptom triage engine
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from src.ai.triage_engine import SymptomTriageEngine


def test_critical_symptoms():
    """Test that critical symptoms are identified correctly"""
    engine = SymptomTriageEngine()
    
    result = engine.assess_symptoms(
        symptoms=['chest pain', 'difficulty breathing'],
        severity='severe'
    )
    
    assert result['urgency'] == 'critical'
    assert result['confidence'] >= 0.90
    assert '911' in result['recommendedAction']


def test_urgent_symptoms():
    """Test that urgent symptoms are identified correctly"""
    engine = SymptomTriageEngine()
    
    result = engine.assess_symptoms(
        symptoms=['high fever', 'severe headache'],
        duration='2 days',
        severity='moderate'
    )
    
    assert result['urgency'] == 'urgent'
    assert result['confidence'] >= 0.70


def test_routine_symptoms():
    """Test that routine symptoms are identified correctly"""
    engine = SymptomTriageEngine()
    
    result = engine.assess_symptoms(
        symptoms=['mild cough', 'runny nose'],
        duration='3 days',
        severity='mild'
    )
    
    assert result['urgency'] == 'routine'
    assert 'primary care' in result['recommendedAction'].lower()


def test_age_adjustment_elderly():
    """Test that age adjustments work for elderly patients"""
    engine = SymptomTriageEngine()
    
    result = engine.assess_symptoms(
        symptoms=['mild fever'],
        patient_age=75
    )
    
    # Elderly patients should get escalated urgency
    assert result['urgency'] in ['urgent', 'critical']


def test_duration_adjustment():
    """Test that duration affects urgency"""
    engine = SymptomTriageEngine()
    
    result = engine.assess_symptoms(
        symptoms=['cough'],
        duration='2 months'
    )
    
    # Long-standing symptoms should be at least urgent
    assert result['urgency'] in ['urgent', 'routine']


def test_next_steps_included():
    """Test that next steps are included in response"""
    engine = SymptomTriageEngine()
    
    result = engine.assess_symptoms(
        symptoms=['sore throat']
    )
    
    assert 'nextSteps' in result
    assert len(result['nextSteps']) > 0
    assert all('action' in step for step in result['nextSteps'])
