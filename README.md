# NVC AI Facilitator - README

## Project Description
An AI-powered web application that facilitates Non-Violent Communication (NVC) practice through guided conversations. The application uses advanced language models to act as an experienced NVC facilitator, helping users work through conflicts and develop empathic communication skills.

## Architecture Overview

### Technology Stack
- **Backend**: Python 3.11+ with FastAPI
- **Frontend**: Vue.js 3 + TypeScript + Tailwind CSS
- **Database**: PostgreSQL 15+ with stored procedures
- **AI Framework**: LangChain with multi-model support
- **Deployment**: AWS (ECS, RDS, CloudFront)
- **Authentication**: JWT with HIPAA compliance

### Project Structure
```
nvc-ai-facilitator/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── models/
│   │   ├── services/
│   │   └── main.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── views/
│   │   ├── services/
│   │   ├── types/
│   │   └── main.ts
│   ├── public/
│   ├── package.json
│   └── Dockerfile
├── database/
│   ├── migrations/
│   └── stored_procedures/
├── infrastructure/
│   ├── terraform/
│   └── docker-compose.yml
├── docs/
└── scripts/
```

## Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose
- AWS CLI (for deployment)

## Development Setup

### 1. Environment Setup
```bash
# Clone repository
git clone <repository-url>
cd nvc-ai-facilitator

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Database Setup
```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Run database migrations
cd backend
alembic upgrade head

# Load initial data (feelings/needs vocabulary)
python scripts/load_initial_data.py
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@localhost:5432/nvc_db
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
JWT_SECRET_KEY=your_jwt_secret
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO
```

### Frontend (.env)
```
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
VITE_APP_NAME=NVC AI Facilitator
```

## Available Scripts

### Backend
```bash
# Start development server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/
isort app/

# Type checking
mypy app/

# Database migration
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint and format
npm run lint
npm run format

# Type checking
npm run type-check
```

## API Documentation
- Development: http://localhost:8000/docs
- Production: https://api.nvc-facilitator.com/docs

## Testing

### Backend Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_nvc_service.py
```

### Frontend Testing
```bash
# Unit tests
npm run test:unit

# E2E tests
npm run test:e2e

# Component tests
npm run test:component
```

## Deployment

### Development Deployment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production Deployment
```bash
# Deploy to AWS
cd infrastructure/terraform
terraform init
terraform plan
terraform apply

# Deploy application
aws ecs update-service --cluster nvc-cluster --service nvc-backend
```

## Security Considerations
- All API endpoints require authentication
- Sensitive data encrypted at rest and in transit
- HIPAA compliance measures implemented
- Regular security audits and dependency updates
- Rate limiting on AI model calls

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit pull request with detailed description

## License
[License details to be determined]

## Support
For technical support or questions:
- Create an issue on GitHub
- Contact the development team
- Review documentation in `/docs`

## Monitoring & Logging
- Application logs: CloudWatch Logs
- Performance metrics: CloudWatch Metrics
- Error tracking: Sentry (optional)
- Uptime monitoring: AWS Route 53 Health Checks