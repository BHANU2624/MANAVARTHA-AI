@echo off
REM Batch script to start the FastAPI server (works without PowerShell execution policy issues)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.

uvicorn main:app --reload --host 0.0.0.0 --port 8000 --reload-exclude "*.pyc" --reload-exclude "__pycache__"

pause

