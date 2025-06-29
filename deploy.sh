#!/bin/bash

# Verbum Production Deployment Script
# This script sets up Verbum for production deployment

echo "🚀 Deploying Verbum Thesaurus App for Production"
echo "================================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    exit 1
fi

# Activate virtual environment
source .venv/bin/activate

# Set production environment variables
export HOST=0.0.0.0
export PORT=${PORT:-5020}

echo "📦 Installing production dependencies..."
pip install -r requirements.txt

echo "🔧 Running setup..."
python setup.py

echo "🧪 Running tests..."
python test.py

if [ $? -ne 0 ]; then
    echo "❌ Tests failed. Deployment aborted."
    exit 1
fi

echo "🌐 Starting production server with Gunicorn..."
echo "Server will be available at http://localhost:${PORT}"
echo "Press Ctrl+C to stop the server"

# Start with Gunicorn for production
gunicorn -w 4 -b ${HOST}:${PORT} --timeout 30 --keep-alive 2 app:app
