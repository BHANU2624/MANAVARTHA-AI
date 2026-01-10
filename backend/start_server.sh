#!/bin/bash

# MANAVARTHA-AI Backend Server Startup Script (Linux/Mac)

set -e  # Exit on error

echo "🚀 Starting MANAVARTHA-AI Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run ./setup.sh first to set up the environment."
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "   Copy .env.example to .env and add your API keys."
    exit 1
fi

# Check for data file
if [ ! -f "data/all_telugu_chunk_embeddings_clean.csv" ]; then
    echo "⚠️  Warning: Data file not found at data/all_telugu_chunk_embeddings_clean.csv"
    echo "   The server may not function properly without this file."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Start the server
echo "✅ Starting server on http://0.0.0.0:8000"
echo "   API Docs: http://localhost:8000/docs"
echo "   Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload --host 0.0.0.0 --port 8000
