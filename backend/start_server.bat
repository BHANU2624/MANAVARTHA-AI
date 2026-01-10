@echo off
REM MANAVARTHA-AI Backend Server Startup Script (Windows)
REM This script starts the FastAPI server (works without PowerShell execution policy issues)

echo ========================================
echo  MANAVARTHA-AI Backend Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo ERROR: Virtual environment not found!
    echo Please run setup.bat first to set up the environment.
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if .env exists
if not exist ".env" (
    echo.
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your API keys.
    echo.
    pause
    exit /b 1
)

REM Check for data file
if not exist "data\all_telugu_chunk_embeddings_clean.csv" (
    echo.
    echo WARNING: Data file not found at data\all_telugu_chunk_embeddings_clean.csv
    echo The server may not function properly without this file.
    echo.
    set /p continue="Continue anyway? (y/n): "
    if /i not "%continue%"=="y" exit /b 1
)

echo.
echo ========================================
echo  Starting FastAPI server...
echo ========================================
echo.
echo Server will be available at:
echo   - API: http://localhost:8000
echo   - API Docs: http://localhost:8000/docs
echo   - Health Check: http://localhost:8000/health
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000 --reload-exclude "*.pyc" --reload-exclude "__pycache__"

pause

