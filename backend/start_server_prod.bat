@echo off
REM Production server startup (no auto-reload, more stable)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server (Production Mode - No Auto-Reload)...
echo Server will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo.

uvicorn main:app --host 0.0.0.0 --port 8000

pause

