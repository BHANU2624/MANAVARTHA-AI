# MANAVARTHA-AI
Telugu News Question Answering System with RAG (Retrieval-Augmented Generation)

## Overview
A multilingual Telugu news question answering system that uses:
- **Flutter** frontend for cross-platform UI
- **FastAPI** backend with RAG engine
- **Cohere** for multilingual embeddings
- **Gemini Flash 2.5** for answer generation
- **FAISS** for vector similarity search

## Prerequisites
- Python 3.8+
- Flutter SDK 3.10+
- Cohere API Key
- Google Gemini API Key

## Backend Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the `backend` directory:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
COHERE_API_KEY=your_cohere_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Prepare Data
Ensure you have the embeddings CSV file at:
```
backend/data/all_telugu_chunk_embeddings_clean.csv
```

### 4. Run Backend Server
```bash
cd backend
python main.py
```

The backend will start on `http://localhost:8000`

## Flutter Frontend Setup

### 1. Get Dependencies
```bash
cd telugu_news_app
flutter pub get
```

### 2. Run Flutter App
For Chrome/Web:
```bash
flutter run -d chrome
```

For other platforms:
```bash
flutter run
```

## API Endpoints

### Health Check
```
GET http://localhost:8000/health
```

### Search/Ask Question
```
GET http://localhost:8000/search?query=your_question_here
```

Example:
```bash
curl "http://localhost:8000/search?query=eroju%20news%20highlights%20emiti"
```

## Architecture

### Flutter Frontend (`telugu_news_app`)
- **main.dart**: Entry point with proper import handling
- **home_screen.dart**: Main UI with search functionality
- **API integration**: Connects to backend at `localhost:8000`

### Backend (`backend`)
- **main.py**: FastAPI server with CORS support
- **rag_engine.py**: RAG implementation with:
  - Cohere for embeddings (`embed-multilingual-v3.0`)
  - Gemini Flash 2.5 for answer generation (`gemini-2.0-flash-exp`)
  - FAISS for vector search
  - Multi-language support (Telugu, English, Romanized Telugu)

## Troubleshooting

### Flutter Compilation Error
If you see `'ByteData' isn't a type` error:
- Ensure you're on the correct branch: `git checkout copilot/fix-byte-data-type-error`
- Run `flutter clean` and `flutter pub get`

### Backend API Errors
If backend returns 404 or model errors:
- Verify your `GEMINI_API_KEY` is valid
- Check that Gemini API is enabled in your Google Cloud Console
- Ensure the backend server is running on port 8000

### Connection Errors in Flutter
If Flutter can't connect to backend:
- Verify backend is running: `curl http://localhost:8000/health`
- Check firewall settings allow localhost connections
- For web, ensure CORS is properly configured in `main.py`

## Recent Updates
- ✅ Fixed Flutter `ByteData` import conflict
- ✅ Migrated from deprecated Cohere `command-r` to Gemini Flash 2.5
- ✅ Added environment variable configuration
- ✅ Improved error handling and logging

## License
Capstone Project
