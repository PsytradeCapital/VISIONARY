#!/bin/bash
echo "🚀 Starting Visionary Backend..."
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Starting FastAPI server..."
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}