# MANAVARTHA-AI Quick Reference Guide

Quick commands and reference for developers working on MANAVARTHA-AI.

## Table of Contents
- [Setup](#setup)
- [Backend Commands](#backend-commands)
- [Frontend Commands](#frontend-commands)
- [Docker Commands](#docker-commands)
- [Common Issues](#common-issues)

## Setup

### Backend Setup (Quick)
```bash
cd backend
./setup.sh           # Linux/Mac
setup.bat            # Windows
```

### Frontend Setup (Quick)
```bash
cd telugu_news_app
flutter pub get
```

## Backend Commands

### Virtual Environment
```bash
# Linux/Mac
source venv/bin/activate
deactivate

# Windows (CMD)
venv\Scripts\activate.bat
deactivate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
deactivate
```

### Run Server
```bash
# Development (auto-reload)
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Using scripts
./start_server.sh    # Linux/Mac
start_server.bat     # Windows
```

### Install/Update Dependencies
```bash
pip install -r requirements.txt
pip install --upgrade -r requirements.txt
```

### Testing
```bash
# Test imports
python -c "import main; import rag_engine; print('OK')"

# Health check
curl http://localhost:8000/health

# Test query
curl "http://localhost:8000/search?query=test"
```

## Frontend Commands

### Run App
```bash
# Web
flutter run -d chrome

# Android
flutter run -d android

# iOS (macOS only)
flutter run -d ios

# Windows
flutter run -d windows

# macOS
flutter run -d macos

# Linux
flutter run -d linux
```

### Build for Production
```bash
# Web
flutter build web --release

# Android APK
flutter build apk --release

# Android App Bundle
flutter build appbundle --release

# iOS
flutter build ios --release

# Windows
flutter build windows --release

# macOS
flutter build macos --release

# Linux
flutter build linux --release
```

### Maintenance
```bash
# Get dependencies
flutter pub get

# Upgrade dependencies
flutter pub upgrade

# Clean build artifacts
flutter clean

# Analyze code
flutter analyze

# Run tests
flutter test

# Check for outdated packages
flutter pub outdated
```

## Docker Commands

### Basic Operations
```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose up -d --build

# Restart
docker-compose restart
```

### Advanced
```bash
# Build without cache
docker-compose build --no-cache

# Remove volumes
docker-compose down -v

# Enter container
docker-compose exec backend bash

# View container stats
docker stats
```

## Common Issues

### Backend: "COHERE_API_KEY not found"
```bash
# Create .env file
cp .env.example .env
# Edit .env and add your API keys
```

### Backend: "CSV file not found"
```bash
# Ensure file exists at:
backend/data/all_telugu_chunk_embeddings_clean.csv
```

### Backend: "Port 8000 already in use"
```bash
# Find and kill process
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows (CMD)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Backend: "ModuleNotFoundError"
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend: "Failed to connect to backend"
```bash
# Ensure backend is running
curl http://localhost:8000/health

# Check API URL in:
# - lib/services/api_service.dart
# - lib/screens/home_screen.dart
```

### Frontend: Build errors
```bash
flutter clean
flutter pub get
flutter pub upgrade
```

### PowerShell Execution Policy Error
```bash
# Use batch file instead
start_server.bat

# Or change policy (admin PowerShell)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Environment Variables

### Required
```env
COHERE_API_KEY=your_cohere_api_key
```

### Optional
```env
GEMINI_API_KEY=your_gemini_api_key
```

## File Locations

### Backend
- Main app: `backend/main.py`
- RAG engine: `backend/rag_engine.py`
- Requirements: `backend/requirements.txt`
- Environment: `backend/.env`
- Data: `backend/data/all_telugu_chunk_embeddings_clean.csv`

### Frontend
- Main app: `telugu_news_app/lib/main.dart`
- Home screen: `telugu_news_app/lib/screens/home_screen.dart`
- API service: `telugu_news_app/lib/services/api_service.dart`
- Dependencies: `telugu_news_app/pubspec.yaml`

## API Endpoints

### Health Check
```
GET http://localhost:8000/health
```

### Search/Ask Question
```
GET http://localhost:8000/search?query=<your_question>
```

### API Documentation
```
GET http://localhost:8000/docs
```

## Useful Links

- [Cohere Dashboard](https://dashboard.cohere.com/api-keys)
- [Gemini API Keys](https://aistudio.google.com/app/apikey)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Flutter Docs](https://docs.flutter.dev/)
- [Docker Docs](https://docs.docker.com/)

## Quick Troubleshooting

1. **Backend won't start** → Check .env file and data file
2. **Frontend can't connect** → Verify backend URL and CORS
3. **Import errors** → Activate virtual environment
4. **Build errors** → Run `flutter clean && flutter pub get`
5. **Permission errors** → Check file permissions (chmod +x for .sh files)

## Development Workflow

1. Make changes to code
2. Test locally (backend: `uvicorn main:app --reload`, frontend: `flutter run`)
3. Run linters/analyzers
4. Commit changes
5. Push to repository
6. Deploy (Docker or manual)

## Support

- Documentation: See README.md and CONTRIBUTING.md
- Issues: https://github.com/BHANU2624/MANAVARTHA-AI/issues
- Contributing: See CONTRIBUTING.md
