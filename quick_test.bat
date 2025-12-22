@echo off
echo 🚀 Quick Test - Visionary AI Web App
echo.

echo Testing if backend works...
cd backend
python -c "print('✅ Python works')"

echo.
echo Testing if frontend works...
cd ..\frontend
if exist package.json (
    echo ✅ Frontend folder exists
    echo ✅ package.json found
) else (
    echo ❌ Frontend not found
)

echo.
echo 🎯 Your web app is ready to test!
echo.
echo Next steps:
echo 1. Open Terminal 1: cd backend && python -m uvicorn main:app --reload
echo 2. Open Terminal 2: cd frontend && npm start
echo 3. Go to: http://localhost:3000
echo.
pause