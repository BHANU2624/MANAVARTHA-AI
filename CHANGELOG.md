# Changelog

All notable changes to the MANAVARTHA-AI project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added - Major Project Setup and Fixes (2026-01-10)

#### Security (Critical)
- Removed hardcoded API keys from `api.py`
- Added environment variable support via `python-dotenv`
- Created `.env.example` files for root and backend directories
- Enhanced `.gitignore` to prevent committing sensitive data (.env files, API keys)
- Added comprehensive security documentation in README

#### Backend
- **Dependencies:**
  - Updated `requirements.txt` with Python 3.12 compatible versions
  - Added missing dependencies: `httpx`, `streamlit`, `requests`
  - Updated version constraints to use flexible ranges (>=) instead of pinned versions
  - Added `google-generativeai>=0.3.0` with proper version
  - Updated `faiss-cpu` from 1.7.4 to >=1.8.0 for Python 3.12 compatibility

- **Code Improvements:**
  - Added proper CORS middleware to `api.py`
  - Improved error handling in `api.py` for missing data files
  - Added validation checks for environment variables
  - Fixed imports to use environment variables consistently

- **Docker Support:**
  - Created `Dockerfile` for containerized backend deployment
  - Created `docker-compose.yml` for orchestration
  - Added `.dockerignore` for efficient builds
  - Included health checks in Docker configuration

- **Scripts:**
  - Created `setup.sh` (Linux/Mac) for automated environment setup
  - Created `setup.bat` (Windows) for automated environment setup
  - Enhanced `start_server.bat` with validation and better messages
  - Created `start_server.sh` (Linux/Mac) with validation

#### Frontend (Flutter)
- **Bug Fixes:**
  - Fixed duplicate `ui` import alias in `main.dart`
  - Removed unnecessary `dart:typed_data` import

- **Configuration:**
  - Updated `pubspec.yaml` SDK constraint from `^3.10.1` to `>=3.10.1 <4.0.0`
  - Verified all dependencies are properly specified

#### Documentation
- **Root Documentation:**
  - Created comprehensive `README.md` with:
    - Full project description and features
    - Architecture diagram
    - Complete setup instructions for backend and frontend
    - API documentation with examples
    - Docker deployment guide
    - Manual deployment guide with systemd configuration
    - Troubleshooting section
    - Security best practices
    - Contributing guidelines
    - Project structure
    - Roadmap

- **Contributing Guidelines:**
  - Created `CONTRIBUTING.md` with:
    - Code of conduct
    - Development setup instructions
    - Bug reporting template
    - Pull request process and template
    - Coding standards for Python (PEP 8) and Dart (Effective Dart)
    - Testing guidelines
    - Documentation standards

- **Backend Documentation:**
  - Updated `backend/README.md` with comprehensive setup instructions
  - Updated `backend/QUICKSTART.md` to reference `.env.example`
  - Documented all environment variables

- **Frontend Documentation:**
  - Created comprehensive `telugu_news_app/README.md` with:
    - Feature list
    - Installation instructions
    - Platform-specific build commands
    - API integration documentation
    - Troubleshooting guide

- **Legal:**
  - Added MIT `LICENSE` file
  - Updated README to reference LICENSE

#### Configuration Files
- **Enhanced `.gitignore`:**
  - Added comprehensive Python exclusions
  - Added Node.js exclusions
  - Added Flutter build artifacts
  - Added IDE-specific files
  - Added OS-specific files
  - Added test and coverage files
  - Added data files (.csv, .index, .faiss)

#### Testing
- Verified all Python imports work correctly
- Confirmed backend dependencies install without errors
- Validated Python syntax across all files
- Ran CodeQL security scan - 0 vulnerabilities found

#### Infrastructure
- Added Docker support for easy deployment
- Added systemd service configuration example
- Created automated setup scripts for Windows and Unix systems
- Added health check endpoints

### Technical Details

#### Python Dependencies Updated
- `google-generativeai`: Now >=0.3.0 (was unversioned)
- `pandas`: Now >=2.1.0 (was 2.1.4)
- `numpy`: Now >=1.24.0 (was 1.26.3)
- `faiss-cpu`: Now >=1.8.0 (was 1.7.4, incompatible with Python 3.12)
- `cohere`: Now >=4.47 (was 4.47)
- Added `httpx>=0.25.0`
- Added `streamlit>=1.30.0`
- Added `requests>=2.31.0`

#### Breaking Changes
None - All changes are backwards compatible

#### Migration Guide
For existing installations:
1. Pull the latest changes
2. Copy `.env.example` to `.env`
3. Move your API keys from hardcoded values to `.env` file
4. Reinstall dependencies: `pip install -r requirements.txt`
5. Verify the data file path: `backend/data/all_telugu_chunk_embeddings_clean.csv`

## [1.0.0] - 2026-01-10

### Initial Release
- FastAPI backend with RAG implementation
- Flutter cross-platform frontend
- Cohere API integration for embeddings
- FAISS vector search
- Multilingual support (Telugu, English, Romanized Telugu)
