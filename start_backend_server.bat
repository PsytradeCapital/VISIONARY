@echo off
echo Starting Visionary AI Backend Server...
echo.

REM Change to the backend directory
cd /d "C:\Users\Martin Mbugua\Desktop\VISIONARY\backend"

echo Current directory: %CD%
echo.

echo Checking if main.py exists...
if exist main.py (
    echo Found main.py - starting server...
    echo.
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo ERROR: main.py not found in backend directory
    echo Please make sure you're in the correct backend directory
    echo.
    dir *.py
)

echo.
pause