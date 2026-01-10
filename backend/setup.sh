#!/bin/bash

# MANAVARTHA-AI Backend Setup Script
# This script sets up the backend development environment

set -e  # Exit on error

echo "🚀 MANAVARTHA-AI Backend Setup"
echo "================================"

# Check Python version
echo ""
echo "📋 Checking Python version..."
python3 --version || { echo "❌ Python 3 not found. Please install Python 3.8+"; exit 1; }

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Setup environment file
echo ""
echo "🔐 Setting up environment variables..."
if [ -f ".env" ]; then
    echo "⚠️  .env file already exists. Skipping creation."
    echo "   If you need to reset it, delete .env and run this script again."
else
    cp .env.example .env
    echo "✅ Created .env file from .env.example"
    echo "⚠️  IMPORTANT: Edit .env and add your API keys:"
    echo "   - COHERE_API_KEY (get from https://dashboard.cohere.com/api-keys)"
    echo "   - GEMINI_API_KEY (get from https://aistudio.google.com/app/apikey)"
fi

# Check for data directory
echo ""
echo "📂 Checking data directory..."
if [ -d "data" ]; then
    echo "✅ Data directory exists"
    if [ -f "data/all_telugu_chunk_embeddings_clean.csv" ]; then
        echo "✅ Data file found"
    else
        echo "⚠️  Data file not found: data/all_telugu_chunk_embeddings_clean.csv"
        echo "   You'll need to add this file to run the application."
    fi
else
    echo "⚠️  Data directory not found. Creating it..."
    mkdir -p data
    echo "✅ Created data directory"
    echo "   Place your CSV file at: data/all_telugu_chunk_embeddings_clean.csv"
fi

# Summary
echo ""
echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your API keys"
echo "2. Place your data file in: data/all_telugu_chunk_embeddings_clean.csv"
echo "3. Activate virtual environment: source venv/bin/activate"
echo "4. Run the server: uvicorn main:app --reload"
echo ""
echo "Or use the start_server.bat script (Windows) or start_server.sh script (Linux/Mac)"
echo ""
