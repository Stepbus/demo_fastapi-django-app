#!/bin/bash

set -e

sleep 4

cd src/
echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting FastAPI + Django..."
uvicorn django_app.asgi:fastapi_app --host 0.0.0.0 --port 8000
