# PowerShell script to start the FastAPI server
# Make sure you have a .env file with COHERE_API_KEY

Write-Host "Activating virtual environment..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1

Write-Host "Starting FastAPI server..." -ForegroundColor Green
Write-Host "Server will be available at: http://localhost:8000" -ForegroundColor Yellow
Write-Host "API docs at: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000

