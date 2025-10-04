# OHIPFORWARD Quick Start Guide

Get OHIPFORWARD up and running in minutes!

## 🚀 Quick Install (3 Steps)

### 1. Clone and Setup
```bash
git clone https://github.com/Islamhassana3/OHIPFORWARD.git
cd OHIPFORWARD
cp .env.example .env
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the System
```bash
# Initialize database
python src/database/init_db.py

# Start backend server
python src/main.py
```

The API will be available at `http://localhost:5000`

## 🎯 Try It Now!

### Test the API
```bash
# Health check
curl http://localhost:5000/api/v1/health

# Symptom triage
curl -X POST http://localhost:5000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough"], "duration": "3 days", "severity": "moderate"}'

# List providers
curl http://localhost:5000/api/v1/providers
```

### Run the Complete Example
```bash
python examples/patient_journey_example.py
```

This will demonstrate a full patient journey:
1. ✅ Patient registration
2. ✅ Symptom assessment  
3. ✅ Provider matching
4. ✅ Appointment scheduling
5. ✅ Transportation booking

## 🧪 Run Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test suite
pytest tests/test_triage_engine.py -v
pytest tests/integration/test_full_journey.py -v
```

## 🐳 Docker Deployment

### Quick Docker Start
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop
docker-compose down
```

## 📊 Access Frontend

### Install and Start Frontend
```bash
cd frontend
npm install
npm start
```

Frontend will be available at `http://localhost:3000`

## 🔑 Key Features

### 1. Symptom Triage
```bash
POST /api/v1/triage
```
- AI-powered assessment
- Urgency classification
- Confidence scoring
- Actionable recommendations

### 2. Appointment Scheduling
```bash
POST /api/v1/appointments
```
- Smart provider matching
- Real-time availability
- Urgency-based priority
- Automated booking

### 3. Provider Search
```bash
GET /api/v1/providers?specialty=cardiology
```
- Filter by specialty
- Sort by rating/wait time
- Real-time availability
- Detailed provider info

### 4. Transportation
```bash
POST /api/v1/transportation
```
- Uber Health integration
- Automated ride booking
- Real-time tracking
- Cost optimization

### 5. Care Monitoring
```bash
GET /api/v1/care-journeys/{patient_id}
GET /api/v1/care-journeys/{patient_id}/gaps
```
- Journey tracking
- Gap identification
- Milestone monitoring
- Outcome tracking

## 📈 System Metrics
```bash
GET /api/v1/metrics
```

Monitor system performance:
- Wait time reduction: **60%**
- Cost savings: **25%**
- Patient satisfaction
- System utilization

## 🔧 Configuration

Edit `.env` file to configure:

```env
# Database
DATABASE_URL=sqlite:///ohipforward.db

# API Keys
UBER_HEALTH_API_KEY=your_key_here
TWILIO_API_KEY=your_key_here

# Server
PORT=5000
DEBUG=false
```

## 📚 Documentation

- **[README.md](README.md)** - Project overview
- **[docs/API.md](docs/API.md)** - Complete API reference
- **[docs/FEATURES.md](docs/FEATURES.md)** - Feature details
- **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment

## 🆘 Troubleshooting

### Database Error
```bash
# Reinitialize database
rm ohipforward.db
python src/database/init_db.py
```

### Port Already in Use
```bash
# Change port in .env
PORT=5001
```

### Import Errors
```bash
# Ensure you're in the project root
cd /path/to/OHIPFORWARD
python src/main.py
```

## 💡 Example Workflows

### Create a Patient
```bash
curl -X POST http://localhost:5000/api/v1/patients \
  -H "Content-Type: application/json" \
  -d '{
    "ohipNumber": "1234567890AB",
    "firstName": "John",
    "lastName": "Doe",
    "dateOfBirth": "1980-05-15",
    "phone": "416-555-0100"
  }'
```

### Assess Symptoms
```bash
curl -X POST http://localhost:5000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{
    "symptoms": ["chest pain", "shortness of breath"],
    "severity": "severe",
    "patientAge": 55
  }'
```

### Schedule Appointment
```bash
curl -X POST http://localhost:5000/api/v1/appointments \
  -H "Content-Type: application/json" \
  -d '{
    "patientId": 1,
    "serviceType": "consultation",
    "urgency": "urgent",
    "preferences": {
      "specialty": "Cardiology"
    }
  }'
```

## 🎓 Learning Resources

### Sample Data
The system comes pre-loaded with:
- 5 healthcare providers
- Various specialties
- Availability schedules
- Rating and review data

### Test Cases
Review `tests/` directory for:
- Unit tests for triage engine
- Integration tests for full workflows
- Example API interactions

## 🚀 Next Steps

1. ⭐ **Star the repository** on GitHub
2. 📖 **Read the full documentation** in `/docs`
3. 🧪 **Run the tests** to understand the system
4. 🎨 **Customize the frontend** to your needs
5. 🏥 **Deploy to production** using deployment guide
6. 🤝 **Contribute** improvements and features

## 📞 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/Islamhassana3/OHIPFORWARD/issues)
- **Documentation**: Check `/docs` directory
- **Examples**: Review `/examples` directory

## ⚡ Performance Targets

OHIPFORWARD is designed to achieve:
- ✅ **60% reduction** in wait times
- ✅ **25% cost savings** through optimization
- ✅ **100% system coverage** for Ontario
- ✅ **Real-time** coordination and updates

---

**Built for Ontario's Healthcare Network** 🏥

Transform fragmented patient journeys into seamless AI-managed experiences!
