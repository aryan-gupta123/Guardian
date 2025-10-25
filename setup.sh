#!/bin/bash

echo "🚀 Setting up Anomaly Detection System..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📥 Installing Node.js dependencies..."
cd frontend
npm install

# Build React app
echo "🏗️ Building React frontend..."
npm run build

# Go back to root
cd ..

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp env.example .env
    echo "✅ Created .env file with SQLite configuration"
fi

# Run Django migrations
echo "🗄️ Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "👤 Creating superuser..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || echo "Superuser already exists"

echo "✅ Setup complete!"
echo ""
echo "To start the development servers:"
echo "1. Backend: python manage.py runserver"
echo "2. Frontend: cd frontend && npm run dev"
echo ""
echo "Access the application at:"
echo "- Django Admin: http://localhost:8000/admin/"
echo "- API: http://localhost:8000/api/"
echo "- Frontend: http://localhost:3000/"

