"""
Main Flask application for OHIPFORWARD API
"""
import os
import sys
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.models import Base, Patient, Provider, Appointment
from src.ai.triage_engine import SymptomTriageEngine
from src.services.appointment_service import AppointmentService
from src.services.transportation_service import TransportationService
from src.services.care_monitoring_service import CareMonitoringService

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ohipforward.db')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Initialize AI engine
triage_engine = SymptomTriageEngine()


def get_db():
    """Get database session"""
    return Session()


@app.route('/')
def index():
    """Root endpoint"""
    return jsonify({
        'name': 'OHIPFORWARD API',
        'version': '1.0.0',
        'description': 'Healthcare coordination system API',
        'status': 'operational'
    })


@app.route('/api/v1/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    })


# =============================================================================
# Symptom Triage Endpoints
# =============================================================================

@app.route('/api/v1/triage', methods=['POST'])
def triage_symptoms():
    """
    POST /api/v1/triage
    Assess patient symptoms and determine urgency
    """
    data = request.json
    
    # Validate input
    if not data.get('symptoms'):
        return jsonify({'error': 'Symptoms are required'}), 400
    
    # Perform triage assessment
    assessment = triage_engine.assess_symptoms(
        symptoms=data['symptoms'],
        duration=data.get('duration'),
        severity=data.get('severity'),
        patient_age=data.get('patientAge')
    )
    
    # Save triage session if patient ID provided
    if data.get('patientId'):
        db = get_db()
        from src.database.models import TriageSession
        
        triage_session = TriageSession(
            patient_id=data['patientId'],
            symptoms=data['symptoms'],
            duration=data.get('duration'),
            severity=data.get('severity'),
            urgency_level=assessment['urgency'],
            ai_confidence=assessment['confidence'],
            recommended_action=assessment['recommendedAction'],
            next_steps=assessment['nextSteps']
        )
        db.add(triage_session)
        db.commit()
        assessment['sessionId'] = triage_session.id
        db.close()
    
    return jsonify(assessment)


# =============================================================================
# Provider Endpoints
# =============================================================================

@app.route('/api/v1/providers', methods=['GET'])
def get_providers():
    """
    GET /api/v1/providers
    Search for healthcare providers
    """
    db = get_db()
    
    # Get query parameters
    specialty = request.args.get('specialty')
    location = request.args.get('location')
    available = request.args.get('available', 'true').lower() == 'true'
    
    # Build query
    query = db.query(Provider)
    
    if specialty:
        query = query.filter(Provider.specialty.ilike(f'%{specialty}%'))
    
    if available:
        query = query.filter(Provider.accepts_new_patients == True)
    
    # Execute query
    providers = query.order_by(
        Provider.rating.desc(),
        Provider.average_wait_time_days.asc()
    ).limit(20).all()
    
    # Format response
    result = {
        'providers': [
            {
                'id': p.id,
                'name': p.name,
                'specialty': p.specialty,
                'phone': p.phone,
                'address': p.address,
                'rating': p.rating,
                'totalReviews': p.total_reviews,
                'waitTime': f'{p.average_wait_time_days} days',
                'acceptsNewPatients': p.accepts_new_patients
            }
            for p in providers
        ]
    }
    
    db.close()
    return jsonify(result)


@app.route('/api/v1/providers/<int:provider_id>', methods=['GET'])
def get_provider(provider_id):
    """Get details for a specific provider"""
    db = get_db()
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    
    if not provider:
        db.close()
        return jsonify({'error': 'Provider not found'}), 404
    
    result = {
        'id': provider.id,
        'name': provider.name,
        'specialty': provider.specialty,
        'phone': provider.phone,
        'email': provider.email,
        'address': provider.address,
        'rating': provider.rating,
        'totalReviews': provider.total_reviews,
        'waitTime': f'{provider.average_wait_time_days} days',
        'acceptsNewPatients': provider.accepts_new_patients
    }
    
    db.close()
    return jsonify(result)


# =============================================================================
# Appointment Endpoints
# =============================================================================

@app.route('/api/v1/appointments', methods=['POST'])
def schedule_appointment():
    """
    POST /api/v1/appointments
    Schedule a new appointment
    """
    data = request.json
    
    # Validate input
    required_fields = ['patientId', 'serviceType', 'urgency']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    db = get_db()
    appointment_service = AppointmentService(db)
    
    # Schedule appointment
    result = appointment_service.schedule_appointment(
        patient_id=data['patientId'],
        service_type=data['serviceType'],
        urgency=data['urgency'],
        preferences=data.get('preferences', {})
    )
    
    db.close()
    
    if result.get('success'):
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/api/v1/appointments/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    """Get appointment details"""
    db = get_db()
    appointment_service = AppointmentService(db)
    
    appointment = appointment_service.get_appointment(appointment_id)
    db.close()
    
    if appointment:
        return jsonify(appointment)
    else:
        return jsonify({'error': 'Appointment not found'}), 404


@app.route('/api/v1/appointments/<int:appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    """Cancel an appointment"""
    db = get_db()
    appointment_service = AppointmentService(db)
    
    success = appointment_service.cancel_appointment(appointment_id)
    db.close()
    
    if success:
        return jsonify({'message': 'Appointment cancelled successfully'})
    else:
        return jsonify({'error': 'Appointment not found'}), 404


# =============================================================================
# Transportation Endpoints
# =============================================================================

@app.route('/api/v1/transportation', methods=['POST'])
def book_transportation():
    """
    POST /api/v1/transportation
    Book transportation for an appointment
    """
    data = request.json
    
    if not data.get('appointmentId') or not data.get('pickupLocation'):
        return jsonify({'error': 'appointmentId and pickupLocation are required'}), 400
    
    db = get_db()
    transport_service = TransportationService(db)
    
    result = transport_service.book_ride(
        appointment_id=data['appointmentId'],
        pickup_location=data['pickupLocation'],
        dropoff_location=data.get('dropoffLocation'),
        scheduled_time=datetime.fromisoformat(data['scheduledTime']) if data.get('scheduledTime') else None
    )
    
    db.close()
    
    if result.get('success'):
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@app.route('/api/v1/transportation/<ride_id>', methods=['GET'])
def get_ride_status(ride_id):
    """Get transportation status"""
    db = get_db()
    transport_service = TransportationService(db)
    
    status = transport_service.get_ride_status(ride_id)
    db.close()
    
    if status:
        return jsonify(status)
    else:
        return jsonify({'error': 'Ride not found'}), 404


# =============================================================================
# Care Monitoring Endpoints
# =============================================================================

@app.route('/api/v1/care-journeys/<int:patient_id>', methods=['GET'])
def get_care_journeys(patient_id):
    """Get care journeys for a patient"""
    db = get_db()
    care_service = CareMonitoringService(db)
    
    journeys = care_service.get_patient_journey(patient_id)
    db.close()
    
    return jsonify({'journeys': journeys})


@app.route('/api/v1/care-journeys/<int:patient_id>/gaps', methods=['GET'])
def identify_care_gaps(patient_id):
    """Identify care gaps for a patient"""
    db = get_db()
    care_service = CareMonitoringService(db)
    
    gaps = care_service.identify_care_gaps(patient_id)
    db.close()
    
    return jsonify({'gaps': gaps})


@app.route('/api/v1/metrics', methods=['GET'])
def get_system_metrics():
    """Get system-wide metrics"""
    db = get_db()
    care_service = CareMonitoringService(db)
    
    metrics = care_service.get_system_metrics()
    db.close()
    
    return jsonify(metrics)


# =============================================================================
# Patient Endpoints
# =============================================================================

@app.route('/api/v1/patients', methods=['POST'])
def create_patient():
    """Create a new patient"""
    data = request.json
    
    required_fields = ['ohipNumber', 'firstName', 'lastName', 'dateOfBirth']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    
    db = get_db()
    
    # Check if patient already exists
    existing = db.query(Patient).filter(
        Patient.ohip_number == data['ohipNumber']
    ).first()
    
    if existing:
        db.close()
        return jsonify({'error': 'Patient with this OHIP number already exists'}), 400
    
    # Create patient
    patient = Patient(
        ohip_number=data['ohipNumber'],
        first_name=data['firstName'],
        last_name=data['lastName'],
        date_of_birth=datetime.fromisoformat(data['dateOfBirth']),
        phone=data.get('phone'),
        email=data.get('email'),
        address=data.get('address'),
        preferred_language=data.get('preferredLanguage', 'en')
    )
    
    db.add(patient)
    db.commit()
    db.refresh(patient)
    
    result = {
        'id': patient.id,
        'ohipNumber': patient.ohip_number,
        'firstName': patient.first_name,
        'lastName': patient.last_name
    }
    
    db.close()
    return jsonify(result), 201


@app.route('/api/v1/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient details"""
    db = get_db()
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    
    if not patient:
        db.close()
        return jsonify({'error': 'Patient not found'}), 404
    
    result = {
        'id': patient.id,
        'ohipNumber': patient.ohip_number,
        'firstName': patient.first_name,
        'lastName': patient.last_name,
        'dateOfBirth': patient.date_of_birth.isoformat(),
        'phone': patient.phone,
        'email': patient.email,
        'address': patient.address
    }
    
    db.close()
    return jsonify(result)


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    host = os.getenv('HOST', '0.0.0.0')
    
    print(f"Starting OHIPFORWARD API server on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    app.run(host=host, port=port, debug=debug)
