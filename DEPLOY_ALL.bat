@echo off
echo 🚀 VISIONARY AI COMPLETE DEPLOYMENT SCRIPT
echo ==========================================
echo.
echo This script will deploy your entire Visionary AI Personal Scheduler:
echo A) Backend to Railway
echo D) Configure AI Services  
echo B) Web App to Vercel
echo C) Mobile App Build
echo.
echo Prerequisites:
echo - Node.js 18+ installed
echo - Git repository on GitHub
echo - Railway account (free)
echo - Vercel account (free)
echo - OpenAI API account with credits
echo.

set /p CONTINUE="Ready to start deployment? (y/n): "
if /i not "%CONTINUE%"=="y" (
    echo Deployment cancelled.
    pause
    exit /b 0
)

echo.
echo ========================================
echo STEP A: DEPLOYING BACKEND TO RAILWAY
echo ========================================
echo.

call deploy-backend.bat
if %errorlevel% neq 0 (
    echo ❌ Backend deployment failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP D: AI SERVICES CONFIGURATION
echo ========================================
echo.

echo ⚠️  IMPORTANT: Configure AI Services
echo.
echo 1. Go to your Railway dashboard
echo 2. Add these environment variables:
echo    - OPENAI_API_KEY=sk-your-openai-key-here
echo    - GOOGLE_CLOUD_API_KEY=your-google-key-here (optional)
echo.
echo 3. Get your OpenAI API key from: https://platform.openai.com
echo 4. Add $10-20 credits to your OpenAI account
echo.

set /p BACKEND_URL="Enter your Railway backend URL (from the previous step): "
set /p AI_CONFIGURED="Have you added the AI API keys to Railway? (y/n): "

if /i not "%AI_CONFIGURED%"=="y" (
    echo ⚠️  Please configure AI services before continuing.
    echo Open your Railway dashboard and add the environment variables.
    pause
)

echo.
echo ========================================
echo STEP B: DEPLOYING WEB APP TO VERCEL
echo ========================================
echo.

echo Using backend URL: %BACKEND_URL%
call deploy-webapp.bat
if %errorlevel% neq 0 (
    echo ❌ Web app deployment failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo STEP C: BUILDING MOBILE APP
echo ========================================
echo.

call build-mobile.bat
if %errorlevel% neq 0 (
    echo ❌ Mobile app build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your Visionary AI Personal Scheduler is now live:
echo.
echo ✅ Backend API: %BACKEND_URL%
echo ✅ Web App: Check your Vercel dashboard for the URL
echo ✅ Mobile App: Check your Expo dashboard for the APK download
echo.
echo 📝 Final Steps:
echo 1. Test all features on your live web app
echo 2. Download and test the mobile APK
echo 3. Update CORS settings if needed
echo 4. Set up monitoring and analytics
echo 5. Prepare for app store submissions
echo.
echo 🚀 Your AI-powered scheduler is ready for users!
echo.
pause