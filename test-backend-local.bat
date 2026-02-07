@echo off
echo ========================================
echo TESTING BACKEND LOCALLY
echo ========================================
echo.

cd backend

echo Starting backend server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
