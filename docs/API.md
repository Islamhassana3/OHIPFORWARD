# OHIPFORWARD API Documentation

## Base URL
```
http://localhost:5000/api/v1
```

## Authentication
Currently, the API is open for development. In production, implement JWT-based authentication.

## Endpoints

### Health Check
```
GET /health
```
Returns system health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:00:00Z"
}
```

---

### Symptom Triage

#### Assess Symptoms
```
POST /triage
```

Analyze patient symptoms and determine urgency level.

**Request Body:**
```json
{
  "symptoms": ["fever", "cough", "difficulty breathing"],
  "duration": "3 days",
  "severity": "moderate",
  "patientId": 123,
  "patientAge": 45
}
```

**Response:**
```json
{
  "urgency": "urgent",
  "confidence": 0.89,
  "recommendedAction": "Visit Emergency Department or Urgent Care within 4 hours",
  "nextSteps": [
    {
      "step": 1,
      "action": "Visit nearest Emergency Department or Urgent Care",
      "priority": "urgent"
    },
    {
      "step": 2,
      "action": "Bring your OHIP card and any medications",
      "priority": "urgent"
    }
  ],
  "assessment": {
    "symptoms": ["fever", "cough", "difficulty breathing"],
    "duration": "3 days",
    "severity": "moderate"
  },
  "sessionId": 456
}
```

---

### Providers

#### Search Providers
```
GET /providers?specialty=cardiology&location=toronto&available=true
```

Find healthcare providers based on criteria.

**Query Parameters:**
- `specialty` (optional): Medical specialty
- `location` (optional): City or region
- `available` (optional): Only show providers accepting new patients (default: true)

**Response:**
```json
{
  "providers": [
    {
      "id": 1,
      "name": "Dr. James Chen",
      "specialty": "Cardiology",
      "phone": "416-555-0102",
      "address": "456 College St, Toronto, ON",
      "rating": 4.9,
      "totalReviews": 203,
      "waitTime": "7.0 days",
      "acceptsNewPatients": true
    }
  ]
}
```

#### Get Provider Details
```
GET /providers/{provider_id}
```

Get detailed information about a specific provider.

---

### Appointments

#### Schedule Appointment
```
POST /appointments
```

Schedule a new appointment with optimal provider matching.

**Request Body:**
```json
{
  "patientId": 123,
  "serviceType": "blood_test",
  "urgency": "routine",
  "preferences": {
    "specialty": "Family Medicine",
    "location": "Toronto",
    "preferredTime": "morning"
  }
}
```

**Response:**
```json
{
  "success": true,
  "appointmentId": 789,
  "provider": {
    "id": 1,
    "name": "Dr. Sarah Smith",
    "specialty": "Family Medicine",
    "rating": 4.8,
    "phone": "416-555-0101"
  },
  "dateTime": "2024-01-20T10:00:00Z",
  "location": "123 University Ave, Toronto, ON",
  "serviceType": "blood_test",
  "urgency": "routine"
}
```

#### Get Appointment
```
GET /appointments/{appointment_id}
```

Retrieve appointment details.

#### Cancel Appointment
```
DELETE /appointments/{appointment_id}
```

Cancel an existing appointment.

---

### Transportation

#### Book Transportation
```
POST /transportation
```

Book Uber Health ride for an appointment.

**Request Body:**
```json
{
  "appointmentId": 789,
  "pickupLocation": {
    "address": "123 Main St, Toronto, ON",
    "latitude": 43.6532,
    "longitude": -79.3832
  },
  "dropoffLocation": {
    "address": "456 Hospital Rd, Toronto, ON"
  },
  "scheduledTime": "2024-01-20T09:30:00Z"
}
```

**Response:**
```json
{
  "success": true,
  "rideId": "uber-1234567890",
  "status": "confirmed",
  "scheduledTime": "2024-01-20T09:30:00Z",
  "pickupLocation": "123 Main St, Toronto, ON",
  "dropoffLocation": "456 Hospital Rd, Toronto, ON",
  "estimatedCost": 15.50,
  "driver": {
    "name": "John Smith",
    "vehicle": "Toyota Camry - ABC 123"
  }
}
```

#### Get Ride Status
```
GET /transportation/{ride_id}
```

Get current status of a booked ride.

---

### Care Monitoring

#### Get Care Journeys
```
GET /care-journeys/{patient_id}
```

Retrieve all care journeys for a patient.

**Response:**
```json
{
  "journeys": [
    {
      "id": 1,
      "patient_id": 123,
      "condition": "Hypertension",
      "status": "active",
      "start_date": "2024-01-01T00:00:00Z",
      "end_date": null,
      "milestones": [
        {
          "timestamp": "2024-01-01T10:00:00Z",
          "type": "triage",
          "description": "Initial symptom assessment"
        },
        {
          "timestamp": "2024-01-05T14:00:00Z",
          "type": "appointment",
          "description": "First consultation with cardiologist"
        }
      ],
      "care_gaps": [],
      "outcomes": {}
    }
  ]
}
```

#### Identify Care Gaps
```
GET /care-journeys/{patient_id}/gaps
```

Identify gaps in patient care (missed appointments, overdue follow-ups, etc.).

**Response:**
```json
{
  "gaps": [
    {
      "journey_id": 1,
      "type": "overdue_followup",
      "severity": "medium",
      "description": "No follow-up appointment in 95 days",
      "last_appointment_date": "2023-10-15T10:00:00Z"
    }
  ]
}
```

---

### System Metrics

#### Get System Metrics
```
GET /metrics
```

Retrieve system-wide performance metrics.

**Response:**
```json
{
  "total_patients": 1523,
  "recent_appointments": 342,
  "average_wait_time_hours": 48.5,
  "wait_time_reduction_percent": 61.2,
  "cost_savings_percent": 25.5,
  "active_care_journeys": 892,
  "system_status": "operational"
}
```

---

### Patients

#### Create Patient
```
POST /patients
```

Register a new patient in the system.

**Request Body:**
```json
{
  "ohipNumber": "1234567890AB",
  "firstName": "John",
  "lastName": "Doe",
  "dateOfBirth": "1980-05-15",
  "phone": "416-555-0100",
  "email": "john.doe@example.com",
  "address": "123 Main St, Toronto, ON",
  "preferredLanguage": "en"
}
```

**Response:**
```json
{
  "id": 123,
  "ohipNumber": "1234567890AB",
  "firstName": "John",
  "lastName": "Doe"
}
```

#### Get Patient
```
GET /patients/{patient_id}
```

Retrieve patient information.

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**
```json
{
  "error": "Description of what went wrong"
}
```

**404 Not Found**
```json
{
  "error": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. In production, implement rate limiting to prevent abuse.

## CORS

CORS is enabled for all origins in development. Restrict this in production.
