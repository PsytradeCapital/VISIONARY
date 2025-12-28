@echo off
echo 🌐 Updating Web App Configuration for Deployment
echo.

set /p BACKEND_URL="Enter your Railway backend URL (e.g., https://backend-production-1a2b.up.railway.app): "

if "%BACKEND_URL%"=="" (
    echo ❌ Error: Backend URL is required
    pause
    exit /b 1
)

echo.
echo Updating web app environment configuration...

cd web_app

echo REACT_APP_API_URL=%BACKEND_URL% > .env.production
echo REACT_APP_API_BASE_URL=%BACKEND_URL%/api/v1 >> .env.production
echo REACT_APP_ENVIRONMENT=production >> .env.production
echo REACT_APP_ENABLE_PWA=true >> .env.production

echo ✅ Web app configuration updated!
echo.
echo Configuration saved to web_app/.env.production:
echo - API URL: %BACKEND_URL%
echo - API Base URL: %BACKEND_URL%/api/v1
echo.
echo 📝 Next steps:
echo 1. Go to vercel.com
echo 2. Import your GitHub repository
echo 3. Set root directory to "web_app"
echo 4. Deploy!
echo.
echo The web app will automatically use the configuration we just created.
echo.
pause