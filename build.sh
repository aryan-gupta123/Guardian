#!/bin/bash

# Build React app
cd frontend
npm install
npm run build
cd ..

# Collect static files
python manage.py collectstatic --noinput

echo "Build completed successfully!"