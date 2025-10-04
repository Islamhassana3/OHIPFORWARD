"""
AI-powered symptom triage engine for OHIPFORWARD
"""
import re
from typing import Dict, List, Tuple


class SymptomTriageEngine:
    """
    Intelligent symptom assessment and urgency classification engine
    """
    
    # Symptom severity mappings
    CRITICAL_SYMPTOMS = {
        'chest pain', 'chest pressure', 'difficulty breathing', 'shortness of breath',
        'severe bleeding', 'severe head injury', 'unconscious', 'loss of consciousness',
        'stroke symptoms', 'numbness', 'slurred speech', 'confusion',
        'severe allergic reaction', 'anaphylaxis', 'seizure', 'severe abdominal pain'
    }
    
    URGENT_SYMPTOMS = {
        'high fever', 'persistent fever', 'severe pain', 'vomiting blood',
        'coughing blood', 'dehydration', 'severe headache', 'vision changes',
        'severe dizziness', 'fainting', 'rapid heartbeat', 'severe nausea',
        'moderate bleeding', 'broken bone', 'severe burn'
    }
    
    ROUTINE_SYMPTOMS = {
        'mild fever', 'cough', 'cold', 'sore throat', 'runny nose',
        'mild headache', 'mild pain', 'rash', 'nausea', 'diarrhea',
        'fatigue', 'muscle aches', 'joint pain', 'back pain'
    }
    
    # Duration severity factors
    DURATION_FACTORS = {
        'hours': 1.2,
        'day': 1.1,
        'days': 1.1,
        'week': 1.0,
        'weeks': 0.9,
        'month': 0.8,
        'months': 0.7
    }
    
    def __init__(self):
        self.confidence_threshold = 0.75
        
    def assess_symptoms(self, symptoms: List[str], duration: str = None, 
                       severity: str = None, patient_age: int = None) -> Dict:
        """
        Assess patient symptoms and determine urgency level
        
        Args:
            symptoms: List of symptom descriptions
            duration: How long symptoms have been present
            severity: Patient-reported severity (mild, moderate, severe)
            patient_age: Patient's age (for age-specific adjustments)
            
        Returns:
            Dictionary with assessment results
        """
        # Normalize symptoms to lowercase
        normalized_symptoms = [s.lower().strip() for s in symptoms]
        
        # Determine base urgency from symptoms
        urgency, confidence = self._determine_urgency(normalized_symptoms)
        
        # Adjust for duration
        if duration:
            urgency, confidence = self._adjust_for_duration(
                urgency, confidence, duration
            )
        
        # Adjust for reported severity
        if severity:
            urgency, confidence = self._adjust_for_severity(
                urgency, confidence, severity
            )
        
        # Adjust for age (elderly and very young may need higher urgency)
        if patient_age:
            urgency, confidence = self._adjust_for_age(
                urgency, confidence, patient_age
            )
        
        # Generate recommendations
        recommended_action = self._get_recommended_action(urgency)
        next_steps = self._get_next_steps(urgency, normalized_symptoms)
        
        return {
            'urgency': urgency,
            'confidence': confidence,
            'recommendedAction': recommended_action,
            'nextSteps': next_steps,
            'assessment': {
                'symptoms': symptoms,
                'duration': duration,
                'severity': severity
            }
        }
    
    def _determine_urgency(self, symptoms: List[str]) -> Tuple[str, float]:
        """Determine urgency level based on symptoms"""
        critical_count = 0
        urgent_count = 0
        routine_count = 0
        
        for symptom in symptoms:
            # Check for critical symptoms
            if any(critical in symptom for critical in self.CRITICAL_SYMPTOMS):
                critical_count += 1
            # Check for urgent symptoms
            elif any(urgent in symptom for urgent in self.URGENT_SYMPTOMS):
                urgent_count += 1
            # Check for routine symptoms
            elif any(routine in symptom for routine in self.ROUTINE_SYMPTOMS):
                routine_count += 1
        
        # Determine urgency and confidence
        if critical_count > 0:
            return 'critical', 0.95
        elif urgent_count > 0:
            confidence = min(0.90, 0.70 + (urgent_count * 0.10))
            return 'urgent', confidence
        elif routine_count > 0:
            confidence = min(0.85, 0.65 + (routine_count * 0.10))
            return 'routine', confidence
        else:
            # Unknown symptoms - default to routine with lower confidence
            return 'routine', 0.60
    
    def _adjust_for_duration(self, urgency: str, confidence: float, 
                            duration: str) -> Tuple[str, float]:
        """Adjust urgency based on symptom duration"""
        duration_lower = duration.lower()
        
        # Extract time unit
        factor = 1.0
        for unit, unit_factor in self.DURATION_FACTORS.items():
            if unit in duration_lower:
                factor = unit_factor
                break
        
        # Adjust confidence
        adjusted_confidence = min(0.99, confidence * factor)
        
        # Very long-standing symptoms might need escalation
        if 'month' in duration_lower or 'months' in duration_lower:
            if urgency == 'routine':
                # Chronic symptoms warrant at least urgent care
                urgency = 'urgent'
                adjusted_confidence = 0.75
        
        return urgency, adjusted_confidence
    
    def _adjust_for_severity(self, urgency: str, confidence: float,
                            severity: str) -> Tuple[str, float]:
        """Adjust urgency based on patient-reported severity"""
        severity_lower = severity.lower()
        
        if 'severe' in severity_lower or 'unbearable' in severity_lower:
            if urgency == 'routine':
                urgency = 'urgent'
            elif urgency == 'urgent':
                urgency = 'critical'
            confidence = min(0.95, confidence + 0.10)
        elif 'moderate' in severity_lower:
            confidence = min(0.90, confidence + 0.05)
        elif 'mild' in severity_lower:
            if urgency == 'urgent':
                confidence *= 0.90
        
        return urgency, confidence
    
    def _adjust_for_age(self, urgency: str, confidence: float,
                       age: int) -> Tuple[str, float]:
        """Adjust urgency based on patient age"""
        # Elderly (65+) or very young (< 2) may need higher urgency
        if age >= 65 or age < 2:
            if urgency == 'routine':
                urgency = 'urgent'
                confidence = min(0.85, confidence)
            else:
                confidence = min(0.95, confidence + 0.05)
        
        return urgency, confidence
    
    def _get_recommended_action(self, urgency: str) -> str:
        """Get recommended action based on urgency level"""
        actions = {
            'critical': 'CALL 911 or visit Emergency Department IMMEDIATELY',
            'urgent': 'Visit Emergency Department or Urgent Care within 4 hours',
            'routine': 'Schedule appointment with primary care provider within 1-3 days',
            'non-urgent': 'Schedule routine appointment within 1-2 weeks'
        }
        return actions.get(urgency, 'Consult with healthcare provider')
    
    def _get_next_steps(self, urgency: str, symptoms: List[str]) -> List[Dict]:
        """Generate next steps based on urgency and symptoms"""
        steps = []
        
        if urgency == 'critical':
            steps.append({
                'step': 1,
                'action': 'Call 911 immediately',
                'priority': 'critical'
            })
            steps.append({
                'step': 2,
                'action': 'Do not drive yourself - wait for ambulance',
                'priority': 'critical'
            })
        elif urgency == 'urgent':
            steps.append({
                'step': 1,
                'action': 'Visit nearest Emergency Department or Urgent Care',
                'priority': 'urgent'
            })
            steps.append({
                'step': 2,
                'action': 'Bring your OHIP card and any medications',
                'priority': 'urgent'
            })
            steps.append({
                'step': 3,
                'action': 'We can arrange transportation if needed',
                'priority': 'normal'
            })
        else:
            steps.append({
                'step': 1,
                'action': 'Schedule appointment with appropriate provider',
                'priority': 'normal'
            })
            steps.append({
                'step': 2,
                'action': 'Monitor symptoms and note any changes',
                'priority': 'normal'
            })
            steps.append({
                'step': 3,
                'action': 'Prepare list of questions for your provider',
                'priority': 'normal'
            })
        
        return steps
