@echo off
echo 🚀 Railway Redeploy Script
echo ========================

echo.
echo 📋 Pre-deployment Checklist:
echo - Backend code is ready
echo - Environment variables are set in Railway dashboard
echo - Database is initialized
echo.

echo 🔍 Checking backend directory...
if not exist "backend\main.py" (
    echo ❌ Error: backend\main.py not found!
    pause
    exit /b 1
)

echo ✅ Backend files found
echo.

echo 📦 Checking requirements.txt...
if not exist "backend\requirements.txt" (
    echo ❌ Error: backend\requirements.txt not found!
    pause
    exit /b 1
)

echo ✅ Requirements file found
echo.

echo 🔧 Checking Railway configuration...
if not exist "backend\railway.json" (
    echo ❌ Error: backend\railway.json not found!
    pause
    exit /b 1
)

echo ✅ Railway config found
echo.

echo 🚀 Ready to redeploy!
echo.
echo Manual steps to complete deployment:
echo.
echo 1. Go to https://railway.app
echo 2. Login with your GitHub account
echo 3. Find your project in the dashboard
echo 4. Click "Deploy" or push changes to trigger redeploy
echo.
echo 🌐 After deployment, test your backend at:
echo https://your-backend-url.railway.app/health
echo.
echo 📝 Don't forget to update your web app's API URL!
echo.

pause