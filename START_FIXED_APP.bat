@echo off
echo ========================================
echo   VISIONARY AI - FIXED VERSION
echo ========================================
echo.

echo This will start both backend and frontend
echo.

echo Step 1: Installing backend dependencies...
cd backend
pip install -q fastapi uvicorn sqlalchemy aiosqlite python-multipart PyPDF2 python-docx python-jose passlib

echo.
echo Step 2: Starting backend server...
start "Visionary Backend" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

echo.
echo Step 3: Starting frontend...
cd ..\frontend
start "Visionary Frontend" cmd /k "npm start"

echo.
echo ========================================
echo   VISIONARY AI IS STARTING!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Two windows will open:
echo 1. Backend server (Python)
echo 2. Frontend app (React)
echo.
echo Close those windows to stop the servers
echo.
pause