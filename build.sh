#!/bin/bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install dependencies with specific flags to avoid compilation issues
pip install --no-cache-dir --upgrade setuptools wheel

# Install numpy first (required for scikit-learn)
pip install --no-cache-dir numpy==1.26.4

# Install scikit-learn with pre-built wheels
pip install --no-cache-dir --only-binary=all scikit-learn==1.4.2

# Install other dependencies
pip install --no-cache-dir -r requirements.txt

# Run Django commands
python manage.py migrate
python manage.py collectstatic --noinput

echo "✅ Build completed successfully!"
