@echo off
REM MANAVARTHA-AI Backend Startup Script for Windows
REM Batch script to start the FastAPI backend server

echo.
echo 🚀 Starting MANAVARTHA-AI Backend...
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ❌ Error: .env file not found!
    echo.
    echo 📝 Please create a .env file with your API keys:
    echo    COHERE_API_KEY=your_cohere_api_key
    echo    GEMINI_API_KEY=your_gemini_api_key
    echo.
    echo You can copy .env.example to .env and edit it:
    echo    copy .env.example .env
    echo.
    exit /b 1
)

REM Check if data directory exists
if not exist "data\all_telugu_chunk_embeddings_clean.csv" (
    echo ⚠️  Warning: Data directory or CSV file not found
    echo 📂 Expected: data\all_telugu_chunk_embeddings_clean.csv
    echo.
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update dependencies
echo 📦 Installing dependencies...
pip install -q -r requirements.txt

echo.
echo ✅ Backend server starting on http://localhost:8000
echo 📚 API Docs available at http://localhost:8000/docs
echo.

REM Start the server
python main.py
