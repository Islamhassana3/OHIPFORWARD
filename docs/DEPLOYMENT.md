# Deployment Guide

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Docker and Docker Compose (for containerized deployment)
- PostgreSQL (for production)

## Local Development

### Backend Setup

1. Clone the repository:
```bash
git clone https://github.com/Islamhassana3/OHIPFORWARD.git
cd OHIPFORWARD
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize database:
```bash
python src/database/init_db.py
```

6. Run the backend:
```bash
python src/main.py
```

The API will be available at `http://localhost:5000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

The frontend will be available at `http://localhost:3000`

## Docker Deployment

### Using Docker Compose

1. Build and start services:
```bash
docker-compose up -d
```

2. Check service status:
```bash
docker-compose ps
```

3. View logs:
```bash
docker-compose logs -f backend
```

4. Stop services:
```bash
docker-compose down
```

### Production Configuration

For production deployment with PostgreSQL:

1. Update `docker-compose.yml` to uncomment the PostgreSQL service

2. Update `.env` file:
```env
DATABASE_URL=postgresql://ohip:your_password@postgres:5432/ohipforward
```

3. Restart services:
```bash
docker-compose down
docker-compose up -d
```

## Cloud Deployment

### AWS Deployment

#### Using EC2

1. Launch an EC2 instance (Ubuntu 22.04 LTS recommended)

2. SSH into the instance:
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

3. Install Docker:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
```

4. Clone and deploy:
```bash
git clone https://github.com/Islamhassana3/OHIPFORWARD.git
cd OHIPFORWARD
docker-compose up -d
```

5. Configure security group to allow:
   - Port 5000 (API)
   - Port 3000 (Frontend)
   - Port 443 (HTTPS)

#### Using Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize EB:
```bash
eb init -p docker ohipforward
```

3. Create environment:
```bash
eb create ohipforward-production
```

4. Deploy:
```bash
eb deploy
```

### Google Cloud Platform

#### Using Cloud Run

1. Build container:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/ohipforward
```

2. Deploy to Cloud Run:
```bash
gcloud run deploy ohipforward \
  --image gcr.io/PROJECT_ID/ohipforward \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure Deployment

#### Using Azure Container Instances

1. Create resource group:
```bash
az group create --name ohipforward-rg --location eastus
```

2. Deploy container:
```bash
az container create \
  --resource-group ohipforward-rg \
  --name ohipforward \
  --image your-registry/ohipforward:latest \
  --dns-name-label ohipforward \
  --ports 5000
```

## Database Migration

### Switching from SQLite to PostgreSQL

1. Export existing data:
```bash
python scripts/export_data.py > data_backup.json
```

2. Update DATABASE_URL in `.env`

3. Initialize new database:
```bash
python src/database/init_db.py
```

4. Import data:
```bash
python scripts/import_data.py < data_backup.json
```

## SSL/TLS Configuration

### Using Let's Encrypt with Nginx

1. Install Nginx and Certbot:
```bash
sudo apt install nginx certbot python3-certbot-nginx
```

2. Configure Nginx (`/etc/nginx/sites-available/ohipforward`):
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

3. Obtain SSL certificate:
```bash
sudo certbot --nginx -d your-domain.com
```

## Monitoring and Logging

### Application Monitoring

1. Install Prometheus and Grafana:
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

2. Access Grafana at `http://localhost:3001`

### Log Management

Logs are stored in:
- Application logs: `/var/log/ohipforward/`
- Docker logs: `docker-compose logs`

Configure log rotation in `/etc/logrotate.d/ohipforward`:
```
/var/log/ohipforward/*.log {
    daily
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 www-data www-data
    sharedscripts
}
```

## Backup and Recovery

### Database Backup

1. Automated backup script:
```bash
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump ohipforward > $BACKUP_DIR/backup_$DATE.sql
```

2. Schedule with cron:
```bash
0 2 * * * /path/to/backup.sh
```

### Disaster Recovery

1. Stop services:
```bash
docker-compose down
```

2. Restore database:
```bash
psql ohipforward < backup_file.sql
```

3. Restart services:
```bash
docker-compose up -d
```

## Performance Optimization

### Caching

Implement Redis caching:

1. Add to docker-compose.yml:
```yaml
redis:
  image: redis:7-alpine
  ports:
    - "6379:6379"
```

2. Update application to use Redis for caching frequently accessed data

### Load Balancing

For high-traffic scenarios, use Nginx as a load balancer:

```nginx
upstream backend {
    server backend1:5000;
    server backend2:5000;
    server backend3:5000;
}

server {
    location / {
        proxy_pass http://backend;
    }
}
```

## Security Checklist

- [ ] Change default SECRET_KEY
- [ ] Enable HTTPS/TLS
- [ ] Implement rate limiting
- [ ] Add authentication/authorization
- [ ] Configure firewall rules
- [ ] Enable database encryption at rest
- [ ] Set up regular security audits
- [ ] Implement HIPAA compliance measures
- [ ] Configure proper CORS policies
- [ ] Set up intrusion detection

## Troubleshooting

### Common Issues

1. **Database connection error**
   - Check DATABASE_URL in .env
   - Verify database is running
   - Check firewall rules

2. **Port already in use**
   - Change PORT in .env
   - Kill process using the port: `lsof -ti:5000 | xargs kill`

3. **Docker build fails**
   - Clear Docker cache: `docker system prune -a`
   - Rebuild: `docker-compose build --no-cache`

## Support

For deployment issues, contact:
- GitHub Issues: https://github.com/Islamhassana3/OHIPFORWARD/issues
- Email: support@ohipforward.ca
