import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database.models import Base, Patient, Provider, ProviderAvailability, SystemMetrics
from dotenv import load_dotenv

load_dotenv()


def init_database():
    """Initialize the database and create all tables"""
    database_url = os.getenv('DATABASE_URL', 'sqlite:///ohipforward.db')
    engine = create_engine(database_url)
    
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")
    
    # Create session for seeding data
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Seed sample data
    seed_sample_data(session)
    
    session.close()
    print("Database initialization complete!")


def seed_sample_data(session):
    """Seed the database with sample data for testing"""
    
    # Check if data already exists
    if session.query(Provider).count() > 0:
        print("Sample data already exists, skipping seeding.")
        return
    
    print("Seeding sample data...")
    
    # Sample Providers
    providers = [
        Provider(
            name="Dr. Sarah Smith",
            specialty="Family Medicine",
            license_number="FM-001-ON",
            phone="416-555-0101",
            email="dr.smith@example.com",
            address="123 University Ave, Toronto, ON",
            latitude=43.6532,
            longitude=-79.3832,
            rating=4.8,
            total_reviews=156,
            average_wait_time_days=2.5,
            accepts_new_patients=True
        ),
        Provider(
            name="Dr. James Chen",
            specialty="Cardiology",
            license_number="CD-002-ON",
            phone="416-555-0102",
            email="dr.chen@example.com",
            address="456 College St, Toronto, ON",
            latitude=43.6574,
            longitude=-79.3987,
            rating=4.9,
            total_reviews=203,
            average_wait_time_days=7.0,
            accepts_new_patients=True
        ),
        Provider(
            name="Dr. Emily Thompson",
            specialty="Emergency Medicine",
            license_number="EM-003-ON",
            phone="416-555-0103",
            email="dr.thompson@example.com",
            address="789 Bay St, Toronto, ON",
            latitude=43.6532,
            longitude=-79.3832,
            rating=4.7,
            total_reviews=98,
            average_wait_time_days=0.5,
            accepts_new_patients=True
        ),
        Provider(
            name="Dr. Michael Patel",
            specialty="Dermatology",
            license_number="DM-004-ON",
            phone="416-555-0104",
            email="dr.patel@example.com",
            address="321 Yonge St, Toronto, ON",
            latitude=43.6629,
            longitude=-79.3957,
            rating=4.6,
            total_reviews=134,
            average_wait_time_days=14.0,
            accepts_new_patients=True
        ),
        Provider(
            name="Dr. Lisa Wong",
            specialty="Orthopedics",
            license_number="OR-005-ON",
            phone="416-555-0105",
            email="dr.wong@example.com",
            address="567 King St, Toronto, ON",
            latitude=43.6481,
            longitude=-79.3799,
            rating=4.9,
            total_reviews=187,
            average_wait_time_days=21.0,
            accepts_new_patients=False
        )
    ]
    
    for provider in providers:
        session.add(provider)
    
    session.commit()
    
    # Add availability slots for providers (Mon-Fri, 9 AM - 5 PM)
    for provider in providers:
        for day in range(5):  # Monday to Friday
            availability = ProviderAvailability(
                provider_id=provider.id,
                day_of_week=day,
                start_time="09:00",
                end_time="17:00",
                is_available=True
            )
            session.add(availability)
    
    session.commit()
    
    # Initialize system metrics
    metrics = SystemMetrics(
        metric_date=datetime.utcnow(),
        total_patients=0,
        total_appointments=0,
        average_wait_time_hours=0.0,
        wait_time_reduction_percent=0.0,
        cost_savings_percent=0.0,
        patient_satisfaction=0.0,
        system_utilization=0.0
    )
    session.add(metrics)
    session.commit()
    
    print(f"Seeded {len(providers)} providers with availability slots")
    print("Sample data seeding complete!")


if __name__ == '__main__':
    init_database()
