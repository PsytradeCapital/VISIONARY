@echo off
echo 🚀 Railway CLI Deployment Script
echo ================================

echo.
echo ✅ You are logged in to Railway
echo.

echo 📁 Navigating to backend directory...
cd backend

echo.
echo 🎯 Step 1: Initialize Railway Project
echo.
echo When prompted:
echo - Project Name: visionary-backend (or leave blank for random)
echo - Select: Empty Project
echo.
pause

railway init

echo.
echo 🎯 Step 2: Set Environment Variables
echo.
echo Setting up environment variables...

railway variables set SECRET_KEY=your-super-secret-jwt-key-make-it-very-long-and-random-123456789
railway variables set DATABASE_URL=sqlite:///./visionary.db
railway variables set DEBUG=False
railway variables set ENVIRONMENT=production

echo.
set /p OPENAI_KEY="Enter your OpenAI API key (sk-...): "
if not "%OPENAI_KEY%"=="" (
    railway variables set OPENAI_API_KEY=%OPENAI_KEY%
)

echo.
echo 🎯 Step 3: Deploy to Railway
echo.
echo Deploying your application...
railway up

echo.
echo 🎯 Step 4: Get Your Deployment URL
echo.
railway status

echo.
echo ✅ Deployment Complete!
echo.
echo 📝 Next steps:
echo 1. Copy your Railway URL from above
echo 2. Run: update-webapp-config.bat
echo 3. Deploy your web app to Vercel
echo.
pause