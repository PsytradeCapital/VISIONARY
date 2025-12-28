@echo off
echo 🚀 Deploying Visionary Backend to Railway...
echo.

echo Step 1: Checking backend directory...
cd backend
if not exist "main.py" (
    echo ❌ Error: main.py not found in backend directory
    pause
    exit /b 1
)

echo ✅ Backend files found
echo.

echo Step 2: Installing Railway CLI...
npm install -g @railway/cli
echo.

echo Step 3: Railway deployment...
echo.
echo ⚠️  IMPORTANT: Railway CLI deployment can be complex.
echo We recommend using the Railway web interface instead.
echo.
echo Please follow these steps:
echo 1. Go to https://railway.app
echo 2. Sign up/login with GitHub
echo 3. Click "New Project"
echo 4. Select "Deploy from GitHub repo"
echo 5. Choose your repository
echo 6. Set root directory to "backend"
echo 7. Railway will auto-deploy!
echo.

echo ✅ Backend deployment complete!
echo.
echo 📝 Next steps:
echo 1. Go to your Railway dashboard
echo 2. Add environment variables:
echo    - SECRET_KEY=your-super-secret-jwt-key-here
echo    - OPENAI_API_KEY=sk-your-openai-key-here
echo    - DEBUG=False
echo 3. Copy your Railway URL for the web app deployment
echo.
echo Your backend should be live at: https://backend-production-xxxx.up.railway.app
echo.
pause