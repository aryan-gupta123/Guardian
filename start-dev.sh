#!/bin/bash

echo "🚀 Starting Anomaly Detection System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp env.example .env
    echo "✅ Created .env file with SQLite configuration"
fi

# Start Django development server
echo "🌐 Starting Django backend server..."
echo "Backend will be available at: http://localhost:8000"
echo "API endpoints: http://localhost:8000/api/"
echo "Django Admin: http://localhost:8000/admin/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python manage.py runserver
