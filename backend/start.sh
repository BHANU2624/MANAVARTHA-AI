#!/bin/bash

# MANAVARTHA-AI Backend Startup Script
# This script starts the FastAPI backend server

echo "🚀 Starting MANAVARTHA-AI Backend..."
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "📝 Please create a .env file with your API keys:"
    echo "   COHERE_API_KEY=your_cohere_api_key"
    echo "   GEMINI_API_KEY=your_gemini_api_key"
    echo ""
    echo "You can copy .env.example to .env and edit it:"
    echo "   cp .env.example .env"
    exit 1
fi

# Check if data directory exists
if [ ! -d "data" ] || [ ! -f "data/all_telugu_chunk_embeddings_clean.csv" ]; then
    echo "⚠️  Warning: Data directory or CSV file not found"
    echo "📂 Expected: data/all_telugu_chunk_embeddings_clean.csv"
    echo ""
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "✅ Backend server starting on http://localhost:8000"
echo "📚 API Docs available at http://localhost:8000/docs"
echo ""

# Start the server
python main.py
