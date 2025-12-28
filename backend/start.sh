#!/bin/bash
set -e

echo "🚀 Starting Visionary Backend..."
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

echo "🔧 Setting up environment..."
export PYTHONPATH="${PYTHONPATH}:."

echo "🌐 Starting FastAPI server on port ${PORT:-8000}..."
exec python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000} --workers 1