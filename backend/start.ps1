# MANAVARTHA-AI Backend Startup Script for Windows
# PowerShell script to start the FastAPI backend server

Write-Host "🚀 Starting MANAVARTHA-AI Backend..." -ForegroundColor Green
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "❌ Error: .env file not found!" -ForegroundColor Red
    Write-Host "📝 Please create a .env file with your API keys:" -ForegroundColor Yellow
    Write-Host "   COHERE_API_KEY=your_cohere_api_key"
    Write-Host "   GEMINI_API_KEY=your_gemini_api_key"
    Write-Host ""
    Write-Host "You can copy .env.example to .env and edit it:" -ForegroundColor Yellow
    Write-Host "   Copy-Item .env.example .env"
    Write-Host ""
    exit 1
}

# Check if data directory exists
if (-not (Test-Path "data") -or -not (Test-Path "data/all_telugu_chunk_embeddings_clean.csv")) {
    Write-Host "⚠️  Warning: Data directory or CSV file not found" -ForegroundColor Yellow
    Write-Host "📂 Expected: data/all_telugu_chunk_embeddings_clean.csv"
    Write-Host ""
}

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"

# Install/update dependencies
Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
pip install -q -r requirements.txt

Write-Host ""
Write-Host "✅ Backend server starting on http://localhost:8000" -ForegroundColor Green
Write-Host "📚 API Docs available at http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

# Start the server
python main.py
