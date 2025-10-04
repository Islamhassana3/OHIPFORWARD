from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    ohip_number = Column(String(12), unique=True, nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    date_of_birth = Column(DateTime, nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    preferred_language = Column(String(10), default='en')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    triage_sessions = relationship('TriageSession', back_populates='patient')
    appointments = relationship('Appointment', back_populates='patient')
    care_journeys = relationship('CareJourney', back_populates='patient')


class TriageSession(Base):
    __tablename__ = 'triage_sessions'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    symptoms = Column(JSON, nullable=False)
    duration = Column(String(100))
    severity = Column(String(50))
    urgency_level = Column(String(20))  # critical, urgent, routine, non-urgent
    ai_confidence = Column(Float)
    recommended_action = Column(Text)
    next_steps = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='triage_sessions')


class Provider(Base):
    __tablename__ = 'providers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    specialty = Column(String(100))
    license_number = Column(String(50), unique=True)
    phone = Column(String(20))
    email = Column(String(100))
    address = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    average_wait_time_days = Column(Float, default=0.0)
    accepts_new_patients = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    availability_slots = relationship('ProviderAvailability', back_populates='provider')
    appointments = relationship('Appointment', back_populates='provider')


class ProviderAvailability(Base):
    __tablename__ = 'provider_availability'
    
    id = Column(Integer, primary_key=True)
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)
    day_of_week = Column(Integer)  # 0=Monday, 6=Sunday
    start_time = Column(String(10))  # HH:MM format
    end_time = Column(String(10))
    is_available = Column(Boolean, default=True)
    
    # Relationships
    provider = relationship('Provider', back_populates='availability_slots')


class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    provider_id = Column(Integer, ForeignKey('providers.id'), nullable=False)
    service_type = Column(String(100))  # blood_test, consultation, imaging, etc.
    scheduled_datetime = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=30)
    status = Column(String(20), default='scheduled')  # scheduled, confirmed, completed, cancelled
    urgency = Column(String(20))  # critical, urgent, routine
    location = Column(Text)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='appointments')
    provider = relationship('Provider', back_populates='appointments')
    transportation = relationship('Transportation', back_populates='appointment', uselist=False)


class Transportation(Base):
    __tablename__ = 'transportation'
    
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=False)
    ride_id = Column(String(100))  # External ride service ID
    pickup_location = Column(Text)
    dropoff_location = Column(Text)
    scheduled_time = Column(DateTime)
    pickup_time = Column(DateTime)
    dropoff_time = Column(DateTime)
    status = Column(String(20), default='pending')  # pending, confirmed, in_progress, completed, cancelled
    cost = Column(Float)
    driver_name = Column(String(100))
    driver_phone = Column(String(20))
    vehicle_info = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointment = relationship('Appointment', back_populates='transportation')


class CareJourney(Base):
    __tablename__ = 'care_journeys'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    condition = Column(String(200))
    status = Column(String(50), default='active')  # active, completed, inactive
    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime)
    milestones = Column(JSON)  # Track key events in the care journey
    care_gaps = Column(JSON)  # Identified gaps in care
    outcomes = Column(JSON)  # Tracked outcomes
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    patient = relationship('Patient', back_populates='care_journeys')


class SystemMetrics(Base):
    __tablename__ = 'system_metrics'
    
    id = Column(Integer, primary_key=True)
    metric_date = Column(DateTime, default=datetime.utcnow)
    total_patients = Column(Integer, default=0)
    total_appointments = Column(Integer, default=0)
    average_wait_time_hours = Column(Float, default=0.0)
    wait_time_reduction_percent = Column(Float, default=0.0)
    cost_savings_percent = Column(Float, default=0.0)
    patient_satisfaction = Column(Float, default=0.0)
    system_utilization = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
