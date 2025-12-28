@echo off
echo 🌐 Deploying Visionary Web App to Vercel...
echo.

set /p BACKEND_URL="Enter your Railway backend URL (e.g., https://backend-production-xxxx.up.railway.app): "

if "%BACKEND_URL%"=="" (
    echo ❌ Error: Backend URL is required
    pause
    exit /b 1
)

echo Step 1: Updating environment configuration...
cd web_app

echo REACT_APP_API_URL=%BACKEND_URL% > .env.production
echo REACT_APP_API_BASE_URL=%BACKEND_URL%/api/v1 >> .env.production
echo REACT_APP_ENVIRONMENT=production >> .env.production

echo ✅ Environment configured
echo.

echo Step 2: Installing dependencies...
npm install
echo.

echo Step 3: Building for production...
npm run build
if %errorlevel% neq 0 (
    echo ❌ Build failed! Check for errors above.
    pause
    exit /b 1
)
echo ✅ Build successful
echo.

echo Step 4: Installing Vercel CLI...
npm install -g vercel
echo.

echo Step 5: Deploying to Vercel...
echo Please login to Vercel in the browser window that opens...
vercel --prod
echo.

echo ✅ Web app deployment complete!
echo.
echo 📝 Next steps:
echo 1. Test your web app at the Vercel URL
echo 2. Update CORS settings in your backend if needed
echo 3. Configure custom domain (optional)
echo.
pause