# OHIPFORWARD System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         OHIPFORWARD System                          │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                          Frontend Layer                              │
├──────────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Patient   │  │  Provider   │  │   Admin     │                 │
│  │   Portal    │  │  Dashboard  │  │   Console   │                 │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                 │
│         │                 │                 │                        │
│         └─────────────────┴─────────────────┘                        │
│                           │                                          │
│                    React.js Frontend                                 │
└───────────────────────────┼──────────────────────────────────────────┘
                            │
                    HTTPS/REST API
                            │
┌───────────────────────────┼──────────────────────────────────────────┐
│                     API Gateway (Flask)                              │
├───────────────────────────┼──────────────────────────────────────────┤
│  ┌────────────────────────┴──────────────────────────┐              │
│  │              RESTful API Endpoints                 │              │
│  │  /triage  /appointments  /providers  /transport   │              │
│  └────────────────────────┬──────────────────────────┘              │
└───────────────────────────┼──────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────────┐
│                     Business Logic Layer                             │
├───────────────────────────┼──────────────────────────────────────────┤
│                            │                                          │
│  ┌─────────────────┐  ┌──┴──────────────┐  ┌──────────────────┐    │
│  │   AI Triage     │  │   Appointment   │  │  Care Monitoring │    │
│  │     Engine      │  │     Service     │  │     Service      │    │
│  │                 │  │                 │  │                  │    │
│  │ • Symptom AI    │  │ • Smart Match   │  │ • Journey Track  │    │
│  │ • Urgency Class │  │ • Scheduling    │  │ • Gap Detection  │    │
│  │ • Confidence    │  │ • Availability  │  │ • Outcomes       │    │
│  └────────┬────────┘  └────────┬────────┘  └────────┬─────────┘    │
│           │                     │                     │              │
│  ┌────────┴─────────────────────┴─────────────────────┴─────────┐   │
│  │              Provider Choice & Transportation                 │   │
│  │  • Provider Matching  • Uber Health  • Real-time Tracking    │   │
│  └───────────────────────────┬──────────────────────────────────┘   │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
┌───────────────────────────────┼──────────────────────────────────────┐
│                        Data Layer                                    │
├───────────────────────────────┼──────────────────────────────────────┤
│                                │                                      │
│  ┌────────────────────────────┴──────────────────────────────────┐  │
│  │                    SQLAlchemy ORM                              │  │
│  └────────────────────────────┬──────────────────────────────────┘  │
│                                │                                      │
│  ┌────────────────────────────┴──────────────────────────────────┐  │
│  │                Database (SQLite/PostgreSQL)                    │  │
│  │                                                                 │  │
│  │  ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────┐    │  │
│  │  │ Patients │ │ Providers │ │ Appoints │ │   Triage     │    │  │
│  │  └──────────┘ └───────────┘ └──────────┘ └──────────────┘    │  │
│  │  ┌──────────┐ ┌───────────┐ ┌──────────┐ ┌──────────────┐    │  │
│  │  │Transport │ │   Care    │ │Provider  │ │   System     │    │  │
│  │  │          │ │ Journeys  │ │Available │ │   Metrics    │    │  │
│  │  └──────────┘ └───────────┘ └──────────┘ └──────────────┘    │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    External Integrations                            │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────┐            │
│  │ Uber Health  │  │   Twilio     │  │     Email      │            │
│  │     API      │  │  (SMS/Voice) │  │     SMTP       │            │
│  └──────────────┘  └──────────────┘  └────────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. Frontend Layer
- **Patient Portal**: Self-service symptom assessment and appointment booking
- **Provider Dashboard**: View schedules, patient info, care journeys
- **Admin Console**: System monitoring, metrics, user management

### 2. API Gateway
- Flask-based REST API
- Request validation and routing
- Authentication and authorization
- Rate limiting and throttling

### 3. Business Logic Layer

#### AI Triage Engine
- Processes patient symptoms
- Determines urgency level
- Calculates confidence scores
- Provides recommendations

#### Appointment Service
- Smart provider matching
- Real-time availability checking
- Urgency-based scheduling
- Conflict resolution

#### Care Monitoring Service
- Tracks patient journeys
- Identifies care gaps
- Monitors outcomes
- Triggers interventions

#### Transportation Service
- Uber Health integration
- Ride scheduling and tracking
- Cost optimization
- Accessibility support

### 4. Data Layer
- SQLAlchemy ORM for database abstraction
- Support for SQLite (dev) and PostgreSQL (prod)
- Efficient indexing and querying
- Data migration support

## Data Flow Examples

### Symptom Triage Flow
```
Patient Input → API → Triage Engine → Database → Response
                        ↓
                  AI Assessment
                  (Urgency + Confidence)
```

### Appointment Booking Flow
```
Patient Request → API → Appointment Service
                         ↓
                   Provider Matching
                         ↓
                   Find Available Slot
                         ↓
                   Create Appointment → Database
                         ↓
                   Book Transportation → Uber Health
                         ↓
                   Send Notifications → Twilio/Email
```

### Care Gap Detection Flow
```
Scheduled Job → Care Monitoring Service
                  ↓
            Query Patient Data
                  ↓
            Analyze Journeys
                  ↓
            Identify Gaps
                  ↓
            Trigger Alerts
                  ↓
            Notify Care Team
```

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers
- Load balancer distribution
- Database read replicas
- Caching layer (Redis)

### Performance Optimization
- Database query optimization
- Connection pooling
- API response caching
- Asynchronous task processing

### High Availability
- Multiple API server instances
- Database replication
- Failover mechanisms
- Health monitoring

## Security Architecture

### Authentication & Authorization
- JWT-based authentication
- Role-based access control (RBAC)
- API key management
- Session management

### Data Protection
- HTTPS/TLS encryption
- Database encryption at rest
- PII data masking
- Audit logging

### Compliance
- HIPAA compliance measures
- Data retention policies
- Privacy controls
- Security audits

## Monitoring & Observability

### Application Monitoring
- Request/response logging
- Error tracking
- Performance metrics
- User analytics

### System Monitoring
- Server health checks
- Database performance
- API latency tracking
- Resource utilization

### Alerting
- Critical error notifications
- Performance degradation alerts
- Capacity warnings
- Security event alerts

## Technology Stack

### Backend
- **Language**: Python 3.8+
- **Framework**: Flask
- **ORM**: SQLAlchemy
- **Database**: SQLite (dev), PostgreSQL (prod)

### Frontend
- **Framework**: React.js
- **Styling**: CSS3
- **HTTP**: Fetch API / Axios

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Docker Compose / Kubernetes
- **Cloud**: AWS / GCP / Azure compatible

### External Services
- **Transportation**: Uber Health API
- **Notifications**: Twilio (SMS), SMTP (Email)
- **Analytics**: Custom metrics

## Deployment Architecture

### Development
```
Developer Machine
  ↓
Python venv + SQLite
  ↓
Flask dev server (port 5000)
```

### Staging
```
Docker Compose
  ↓
Backend Container + PostgreSQL
  ↓
Load Testing Environment
```

### Production
```
Cloud Load Balancer
  ↓
Multiple API Servers (Auto-scaling)
  ↓
PostgreSQL Primary + Read Replicas
  ↓
Redis Cache Layer
  ↓
CDN for Static Assets
```

## Future Architecture Enhancements

### Phase 2
- Microservices architecture
- Event-driven processing
- Message queue (RabbitMQ/Kafka)
- Real-time notifications (WebSockets)

### Phase 3
- Machine learning pipeline
- Advanced analytics platform
- Multi-region deployment
- Edge computing for latency reduction
