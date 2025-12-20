@echo off
echo Starting Visionary Backend - Simple Mode...
echo.

cd backend

echo Installing Python dependencies...
pip install fastapi uvicorn

echo.
echo Starting FastAPI server (Simple Mode)...
echo Backend will be available at: http://localhost:8000
echo Visit http://localhost:8000/docs-redirect for info
echo.

python simple_main.py

pause