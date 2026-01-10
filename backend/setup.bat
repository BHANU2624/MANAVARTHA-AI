@echo off
REM MANAVARTHA-AI Backend Setup Script (Windows)
REM This script sets up the backend development environment

echo ========================================
echo  MANAVARTHA-AI Backend Setup
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist "venv\" (
    echo WARNING: Virtual environment already exists. Skipping creation.
) else (
    python -m venv venv
    echo Virtual environment created successfully!
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Setup environment file
echo Setting up environment variables...
if exist ".env" (
    echo WARNING: .env file already exists. Skipping creation.
    echo          If you need to reset it, delete .env and run this script again.
) else (
    copy .env.example .env >nul
    echo Created .env file from .env.example
    echo.
    echo IMPORTANT: Edit .env and add your API keys:
    echo   - COHERE_API_KEY (get from https://dashboard.cohere.com/api-keys)
    echo   - GEMINI_API_KEY (get from https://aistudio.google.com/app/apikey)
)
echo.

REM Check for data directory
echo Checking data directory...
if exist "data\" (
    echo Data directory exists.
    if exist "data\all_telugu_chunk_embeddings_clean.csv" (
        echo Data file found!
    ) else (
        echo WARNING: Data file not found: data\all_telugu_chunk_embeddings_clean.csv
        echo          You'll need to add this file to run the application.
    )
) else (
    echo WARNING: Data directory not found. Creating it...
    mkdir data
    echo Created data directory.
    echo Place your CSV file at: data\all_telugu_chunk_embeddings_clean.csv
)
echo.

REM Summary
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env and add your API keys
echo 2. Place your data file in: data\all_telugu_chunk_embeddings_clean.csv
echo 3. Run the server using: start_server.bat
echo.
echo Or activate the virtual environment manually:
echo   venv\Scripts\activate.bat
echo Then run:
echo   uvicorn main:app --reload
echo.

pause
