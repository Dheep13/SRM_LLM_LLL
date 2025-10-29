# Quick Start Scripts for LawBot

## Backend Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run backend
python backend/main.py
```

## Frontend Setup
```bash
# Install dependencies
cd frontend
npm install

# Run frontend
npm start
```

## Docker Setup
```bash
# Build and run with Docker Compose
docker-compose up --build

# Run in background
docker-compose up -d --build
```

## Development Mode
```bash
# Terminal 1: Backend
python backend/main.py

# Terminal 2: Frontend
cd frontend && npm start
```

## Production Deployment
```bash
# Build production images
docker-compose -f docker-compose.prod.yml up --build

# Deploy to cloud (example with AWS)
aws ecs create-service --cluster lawbot-cluster --service-name lawbot-service
```

## Testing
```bash
# Test backend API
curl http://localhost:8000/api/health

# Test frontend
open http://localhost:3000
```

## Troubleshooting
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down
docker-compose up --build --force-recreate
```
