"""
Example: Complete patient care journey using OHIPFORWARD

This script demonstrates a full patient workflow from symptom triage
to appointment scheduling and care monitoring.
"""
import requests
import json
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:5000/api/v1"


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_json(data):
    """Pretty print JSON data"""
    print(json.dumps(data, indent=2))


def main():
    """Run complete patient journey example"""
    
    print_section("OHIPFORWARD Patient Journey Example")
    
    # Step 1: Create a patient
    print_section("Step 1: Register Patient")
    patient_data = {
        "ohipNumber": "9876543210XY",
        "firstName": "Jane",
        "lastName": "Smith",
        "dateOfBirth": "1985-03-15",
        "phone": "416-555-0200",
        "email": "jane.smith@example.com",
        "address": "456 Queen St, Toronto, ON",
        "preferredLanguage": "en"
    }
    
    response = requests.post(f"{BASE_URL}/patients", json=patient_data)
    if response.status_code == 201:
        patient = response.json()
        print("✓ Patient registered successfully:")
        print_json(patient)
        patient_id = patient['id']
    else:
        print(f"✗ Error: {response.json()}")
        return
    
    # Step 2: Symptom Triage
    print_section("Step 2: Symptom Triage Assessment")
    triage_data = {
        "symptoms": ["fever", "sore throat", "fatigue"],
        "duration": "4 days",
        "severity": "moderate",
        "patientId": patient_id,
        "patientAge": 38
    }
    
    response = requests.post(f"{BASE_URL}/triage", json=triage_data)
    if response.status_code == 200:
        assessment = response.json()
        print("✓ Triage assessment completed:")
        print(f"  Urgency: {assessment['urgency'].upper()}")
        print(f"  Confidence: {assessment['confidence'] * 100:.1f}%")
        print(f"  Recommendation: {assessment['recommendedAction']}")
        print("\n  Next Steps:")
        for step in assessment['nextSteps']:
            print(f"    {step['step']}. {step['action']}")
    else:
        print(f"✗ Error: {response.json()}")
        return
    
    # Step 3: Find Providers
    print_section("Step 3: Search for Available Providers")
    response = requests.get(f"{BASE_URL}/providers?specialty=Family Medicine&available=true")
    if response.status_code == 200:
        providers = response.json()['providers']
        print(f"✓ Found {len(providers)} available providers:")
        for provider in providers[:3]:  # Show top 3
            print(f"\n  {provider['name']}")
            print(f"    Specialty: {provider['specialty']}")
            print(f"    Rating: {provider['rating']} ⭐ ({provider['totalReviews']} reviews)")
            print(f"    Wait Time: {provider['waitTime']}")
            print(f"    Address: {provider['address']}")
    else:
        print(f"✗ Error: {response.json()}")
        return
    
    # Step 4: Schedule Appointment
    print_section("Step 4: Schedule Appointment")
    appointment_data = {
        "patientId": patient_id,
        "serviceType": "consultation",
        "urgency": assessment['urgency'],
        "preferences": {
            "specialty": "Family Medicine",
            "location": "Toronto"
        }
    }
    
    response = requests.post(f"{BASE_URL}/appointments", json=appointment_data)
    if response.status_code == 201:
        appointment = response.json()
        print("✓ Appointment scheduled successfully:")
        print(f"  Appointment ID: {appointment['appointmentId']}")
        print(f"  Provider: {appointment['provider']['name']}")
        print(f"  Specialty: {appointment['provider']['specialty']}")
        print(f"  Date/Time: {appointment['dateTime']}")
        print(f"  Location: {appointment['location']}")
        appointment_id = appointment['appointmentId']
    else:
        print(f"✗ Error: {response.json()}")
        return
    
    # Step 5: Book Transportation
    print_section("Step 5: Book Transportation")
    transport_data = {
        "appointmentId": appointment_id,
        "pickupLocation": {
            "address": "456 Queen St, Toronto, ON",
            "latitude": 43.6532,
            "longitude": -79.3832
        },
        "scheduledTime": appointment['dateTime']
    }
    
    response = requests.post(f"{BASE_URL}/transportation", json=transport_data)
    if response.status_code == 201:
        ride = response.json()
        print("✓ Transportation booked successfully:")
        print(f"  Ride ID: {ride['rideId']}")
        print(f"  Status: {ride['status']}")
        print(f"  Pickup: {ride['pickupLocation']}")
        print(f"  Scheduled Time: {ride['scheduledTime']}")
        print(f"  Estimated Cost: ${ride['estimatedCost']:.2f}")
        if ride.get('driver'):
            print(f"  Driver: {ride['driver'].get('name', 'TBD')}")
    else:
        print(f"✗ Error: {response.json()}")
    
    # Step 6: View System Metrics
    print_section("Step 6: System Performance Metrics")
    response = requests.get(f"{BASE_URL}/metrics")
    if response.status_code == 200:
        metrics = response.json()
        print("✓ System metrics retrieved:")
        print(f"  Total Patients: {metrics['total_patients']}")
        print(f"  Recent Appointments: {metrics['recent_appointments']}")
        print(f"  Average Wait Time: {metrics['average_wait_time_hours']:.1f} hours")
        print(f"  Wait Time Reduction: {metrics['wait_time_reduction_percent']:.1f}%")
        print(f"  Cost Savings: {metrics['cost_savings_percent']:.1f}%")
        print(f"  System Status: {metrics['system_status'].upper()}")
    else:
        print(f"✗ Error: {response.json()}")
    
    print_section("Journey Complete!")
    print("\nPatient journey completed successfully:")
    print("  ✓ Patient registered")
    print("  ✓ Symptoms assessed")
    print("  ✓ Provider matched")
    print("  ✓ Appointment scheduled")
    print("  ✓ Transportation arranged")
    print("\nOHIPFORWARD is working to streamline your healthcare experience!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n✗ Error: Cannot connect to API server.")
        print("  Make sure the server is running: python src/main.py")
    except Exception as e:
        print(f"\n✗ Error: {e}")
