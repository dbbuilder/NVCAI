# NVC AI Facilitator - README

## Project Description
An AI-powered web and mobile application that facilitates Non-Violent Communication (NVC) practice through guided conversations. The application uses advanced language models to act as an experienced NVC facilitator, helping users work through conflicts and develop empathic communication skills across all platforms.

## Architecture Overview

### Technology Stack
- **Backend**: Python 3.11+ with FastAPI
- **Web Frontend**: React 18+ with TypeScript + Tailwind CSS
- **Mobile Apps**: React Native with TypeScript (iOS & Android)
- **Shared Code**: TypeScript libraries for services, types, and utilities
- **Database**: PostgreSQL 15+ with stored procedures
- **AI Framework**: LangChain with multi-model support
- **Deployment**: AWS (ECS, RDS, CloudFront) + App Store/Play Store
- **Authentication**: JWT with HIPAA compliance

### Project Structure
```
nvc-ai-facilitator/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── api/               # API endpoints
│   │   ├── core/              # Configuration and security
│   │   ├── database/          # Database connection
│   │   ├── models/            # SQLAlchemy models
│   │   ├── services/          # Business logic services
│   │   └── main.py           # FastAPI application
│   ├── alembic/              # Database migrations
│   ├── tests/                # Backend tests
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile           # Backend container
├── frontend/                  # React web application
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── hooks/            # Custom React hooks
│   │   ├── pages/            # Page components
│   │   ├── store/            # Redux Toolkit store
│   │   ├── services/         # API services (links to shared)
│   │   ├── types/            # TypeScript types (links to shared)
│   │   └── utils/            # Utilities (links to shared)
│   ├── public/
│   ├── package.json          # Web dependencies
│   └── Dockerfile           # Frontend container
├── mobile/                   # React Native mobile app
│   ├── src/
│   │   ├── components/       # Mobile-specific components
│   │   ├── screens/          # Mobile screens
│   │   ├── navigation/       # React Navigation setup
│   │   ├── hooks/            # Mobile-specific hooks
│   │   ├── services/         # API services (links to shared)
│   │   ├── types/            # TypeScript types (links to shared)
│   │   └── utils/            # Utilities (links to shared)
│   ├── android/              # Android native code
│   ├── ios/                  # iOS native code
│   └── package.json          # Mobile dependencies
├── shared/                   # Shared code between web and mobile
│   ├── types/                # TypeScript type definitions
│   ├── services/             # API and business logic services
│   ├── utils/                # Utility functions
│   └── constants/            # Shared constants
├── database/
│   ├── migrations/           # Database schema changes
│   ├── stored_procedures/    # PostgreSQL stored procedures
│   └── seed_data/            # Initial data
├── infrastructure/
│   ├── terraform/            # AWS infrastructure as code
│   ├── docker/               # Docker configurations
│   └── scripts/              # Deployment scripts
├── docs/                     # Documentation
└── scripts/                  # Development scripts
```

## Prerequisites
- **Backend**: Python 3.11+, PostgreSQL 15+
- **Web**: Node.js 18+, npm/yarn
- **Mobile**: React Native CLI, Android Studio, Xcode (for iOS)
- **Deployment**: Docker, AWS CLI
- **Development**: Git, VS Code (recommended)

## Development Setup

### 1. Repository Setup
```bash
# Clone repository
git clone https://github.com/dbbuilder/NVCAI.git
cd NVCAI

# Install shared dependencies and link shared modules
cd shared && npm install && npm run build
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys and database settings

# Set up database
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Web Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Link shared modules
npm link ../shared

# Configure environment
cp .env.example .env.local
# Edit .env.local with your API settings

# Start development server
npm start
```

### 4. Mobile App Setup
```bash
cd mobile

# Install dependencies
npm install

# Link shared modules
npm link ../shared

# iOS setup (macOS only)
cd ios && pod install && cd ..

# Start Metro bundler
npm start

# Run on iOS (in separate terminal)
npm run ios

# Run on Android (in separate terminal)
npm run android
```

### 5. Database Setup
```bash
# Start PostgreSQL with Docker
cd infrastructure
docker-compose up -d postgres

# Run database migrations
cd ../backend
alembic upgrade head

# Load initial NVC data
python scripts/load_nvc_data.py
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://nvc_user:nvc_password@localhost:5432/nvc_db
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
JWT_SECRET_KEY=your_super_secure_jwt_secret_key_here
JWT_ALGORITHM=HS256
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8081"]
LOG_LEVEL=INFO
```

### Web Frontend (.env.local)
```
REACT_APP_API_BASE_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_APP_NAME=NVC AI Facilitator
REACT_APP_VERSION=1.0.0
```

### Mobile App (.env)
```
API_BASE_URL=http://localhost:8000
WS_URL=ws://localhost:8000
APP_NAME=NVC AI Facilitator
VERSION=1.0.0
```

## Available Scripts

### Backend
```bash
# Start development server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/ && isort app/

# Type checking
mypy app/

# Database migration
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Web Frontend
```bash
# Development server
npm start

# Build for production
npm run build

# Run tests
npm test

# Lint and format
npm run lint && npm run format

# Type checking
npm run type-check
```

### Mobile App
```bash
# Start Metro bundler
npm start

# Run on iOS
npm run ios

# Run on Android
npm run android

# Build for production (iOS)
npm run build:ios

# Build for production (Android)
npm run build:android

# Run tests
npm test
```

### Shared Libraries
```bash
cd shared

# Build shared libraries
npm run build

# Watch for changes during development
npm run watch

# Run tests
npm test
```

## Code Sharing Strategy

### Shared Components (~80% code reuse)
```typescript
// shared/services/nvc.service.ts
export class NVCService {
  async facilitateStep(step: NVCStep, userInput: string): Promise<AIResponse> {
    // Shared business logic for both web and mobile
  }
}

// shared/types/nvc.types.ts
export interface ConversationSession {
  id: string;
  userId: string;
  currentStep: NVCStep;
  messages: Message[];
  createdAt: Date;
}
```

### Platform-Specific UI
```typescript
// frontend/src/components/ConversationInterface.tsx (Web)
export const ConversationInterface: React.FC = () => {
  return (
    <div className="flex flex-col h-screen">
      <ChatHeader />
      <MessageList />
      <MessageInput />
    </div>
  );
};

// mobile/src/screens/ConversationScreen.tsx (Mobile)
export const ConversationScreen: React.FC = () => {
  return (
    <SafeAreaView style={styles.container}>
      <ChatHeader />
      <MessageList />
      <MessageInput />
    </SafeAreaView>
  );
};
```

## Testing Strategy

### Backend Testing
```bash
# Run all tests with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_nvc_service.py

# Integration tests
pytest tests/integration/
```

### Frontend Testing (Web & Mobile)
```bash
# Unit tests
npm test

# E2E tests (web)
npm run test:e2e

# Component tests
npm run test:component

# Cross-platform shared logic tests
cd shared && npm test
```

## Deployment

### Development Environment
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### Production Deployment

#### Backend & Web (AWS)
```bash
# Deploy infrastructure
cd infrastructure/terraform
terraform init && terraform plan && terraform apply

# Deploy applications
docker build -t nvc-backend backend/
docker build -t nvc-frontend frontend/
aws ecs update-service --cluster nvc-cluster --service nvc-backend
```

#### Mobile Apps
```bash
# iOS (requires macOS and Xcode)
cd mobile
npm run build:ios
# Follow iOS app store submission process

# Android
npm run build:android
# Follow Google Play store submission process
```

## API Documentation
- **Development**: http://localhost:8000/docs
- **Production**: https://api.nvc-facilitator.com/docs

## Mobile App Features

### Native Capabilities
- **Voice Recording**: Practice NVC conversations with voice
- **Push Notifications**: Session reminders and progress updates
- **Offline Mode**: Continue practice without internet
- **Biometric Auth**: Face ID / Touch ID for secure access
- **Background Sync**: Sync data when app returns online

### Cross-Platform Features
- **Real-time Chat**: WebSocket-based AI conversations
- **Progress Tracking**: Visual NVC skill development
- **Research Participation**: Opt-in data collection
- **Session History**: Review past NVC practice sessions
- **Customizable Interface**: Adapt to user preferences

## Security & Compliance
- **HIPAA Ready**: End-to-end encryption for sensitive conversations
- **JWT Authentication**: Secure token-based authentication
- **Data Minimization**: Collect only necessary research data
- **Audit Logging**: Comprehensive access and change tracking
- **App Store Security**: Native mobile security features

## Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make changes with tests
4. Ensure all platforms work: `npm run test:all`
5. Submit pull request with detailed description

## License
[License details to be determined]

## Support & Community
- **GitHub Issues**: Bug reports and feature requests
- **Documentation**: Comprehensive guides in `/docs`
- **Development Chat**: [Link to developer community]
- **User Support**: [Link to user support]

## Monitoring & Analytics
- **Backend**: CloudWatch Logs and Metrics
- **Web**: Google Analytics + Custom dashboards
- **Mobile**: Firebase Analytics + Crashlytics
- **Research**: Custom analytics for NVC effectiveness studies