# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NVC AI Facilitator is an AI-powered web and mobile application that facilitates Non-Violent Communication (NVC) practice through guided conversations. This is a React + React Native cross-platform application with a Python FastAPI backend.

**Current Status**: Project has migrated from Vue.js to React + React Native architecture for optimal cross-platform code sharing (80-90% reuse between web and mobile).

## Technology Stack

- **Backend**: Python 3.11+ with FastAPI, LangChain for AI, PostgreSQL database
- **Web Frontend**: React 18+ with TypeScript + Tailwind CSS  
- **Mobile Apps**: React Native with TypeScript (iOS & Android)
- **Shared Code**: TypeScript libraries in `/shared` directory
- **AI Models**: Multi-model support (OpenAI, Anthropic, Google) via LangChain

## Development Commands

### Backend (Python FastAPI)
```bash
cd backend

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing
pytest
pytest --cov=app tests/  # with coverage

# Code formatting and linting
black app/ && isort app/
mypy app/

# Database migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
```

### Shared Libraries (Critical for cross-platform)
```bash
cd shared

# Build shared TypeScript libraries (REQUIRED before frontend/mobile)
npm install
npm run build

# Development with auto-rebuild
npm run watch

# Testing
npm test
```

### Web Frontend (React)
```bash
cd frontend

# Setup (after shared libraries are built)
npm install
npm link ../shared

# Development server
npm start

# Production build
npm run build

# Testing and quality
npm test
npm run lint && npm run format
npm run type-check
```

### Mobile App (React Native)
```bash
cd mobile

# Setup (after shared libraries are built)
npm install
npm link ../shared

# iOS setup (macOS only)
cd ios && pod install && cd ..

# Development
npm start  # Metro bundler
npm run ios     # iOS simulator
npm run android # Android emulator

# Production builds
npm run build:ios
npm run build:android

# Testing
npm test
npm run lint:fix
npm run type-check
```

## Architecture Key Points

### Cross-Platform Code Sharing
- **Shared Directory**: Contains 80-90% of business logic, types, services, and utilities
- **Platform-Specific UI**: Only UI components differ between web (React) and mobile (React Native)
- **Build Dependencies**: Always build `shared` libraries FIRST before frontend or mobile
- **Linking**: Both frontend and mobile projects link to shared libraries via `npm link`

### Backend Structure
```
backend/
├── app/
│   ├── api/          # FastAPI route handlers by domain
│   ├── core/         # Configuration, security, logging
│   ├── database/     # SQLAlchemy models and session management  
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas for API validation
│   ├── services/     # Business logic services
│   └── main.py       # FastAPI application entry point
├── alembic/          # Database migrations
├── tests/            # Backend tests
└── requirements.txt  # Python dependencies
```

### Frontend Architecture Patterns
- **Shared Services**: API clients, WebSocket handlers, NVC business logic
- **Shared Types**: TypeScript interfaces for all data models  
- **Platform UI**: Web uses Tailwind CSS, Mobile uses React Native StyleSheet
- **State Management**: Redux Toolkit (shared logic, platform-specific UI state)

## Critical Development Notes

### Shared Library Workflow
1. **ALWAYS** build shared libraries first: `cd shared && npm run build`
2. Changes to shared code require rebuild: `npm run build` or `npm run watch`
3. Both frontend and mobile consume shared libraries via `npm link`

### Mobile-Specific Features
- Biometric authentication (Face ID, Touch ID)
- Push notifications  
- Voice recording for NVC practice
- Offline mode with background sync
- Native navigation and gestures

### AI/LangChain Integration
- Multi-model support: OpenAI, Anthropic, Google
- NVC-specific prompting and conversation flow
- Research data collection for NVC effectiveness studies
- Real-time conversation facilitation

### Database and Environment
- PostgreSQL with stored procedures
- Alembic for migrations
- Environment variables for API keys (OpenAI, Anthropic, Google)
- HIPAA compliance considerations for conversation data

## Testing Strategy

- **Backend**: pytest with coverage, integration tests for AI services
- **Shared**: Jest for TypeScript business logic (critical for cross-platform)
- **Frontend**: React Testing Library, E2E with browser automation
- **Mobile**: Jest + Detox for cross-platform mobile testing

## Common Development Tasks

### Adding New Features
1. Define types in `shared/types/`
2. Implement business logic in `shared/services/`  
3. Create platform-specific UI components
4. Add backend API endpoints if needed
5. Write tests for shared logic first

### Debugging Cross-Platform Issues
- Check shared library build: `cd shared && npm run build`
- Verify linking: `npm ls` in frontend/mobile should show shared dependency
- Test shared logic independently: `cd shared && npm test`

### AI Model Integration
- LangChain configuration in `backend/app/core/config.py`
- Model-specific services in `backend/app/services/`
- Conversation state management in shared libraries

## Environment Setup Requirements

- **Python 3.11+** for backend
- **Node.js 18+** for all TypeScript projects
- **React Native CLI** for mobile development
- **PostgreSQL 15+** for database
- **Xcode** (macOS only) for iOS development
- **Android Studio** for Android development

## AI Integration Status

### OpenAI Integration (WORKING)
- **API Key**: Configured in `/backend/.env` 
- **Model**: GPT-4o-mini (60% cheaper + superior performance vs GPT-3.5-turbo)
- **Endpoint**: `/api/v1/nvc/conversation` with OpenAI-powered responses
- **Fallback**: Rule-based logic when OpenAI unavailable
- **Test UI**: Available at `http://localhost:19000/test`

### Quick Test Commands
```bash
# Start backend (port 19000)
cd backend && export PYTHONPATH=/mnt/d/dev2/nvcai/backend && source venv/bin/activate && python app/main.py

# Test OpenAI NVC conversation
curl -X POST -H "Content-Type: application/json" \
  -d '{"message":"I noticed my colleague interrupted me during the meeting"}' \
  http://localhost:19000/api/v1/nvc/conversation

# Access test UI
open http://localhost:19000/test
```

The architecture prioritizes code reuse and native mobile performance while maintaining a unified development experience across all platforms.