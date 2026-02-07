@echo off
echo ========================================
echo REAL DEPLOYMENT - NO DEMO MODE
echo ========================================
echo.

echo Step 1: Get Gemini API Key (FREE)
echo.
echo 1. Go to: https://makersuite.google.com/app/apikey
echo 2. Click "Create API Key"
echo 3. Copy the key (starts with AIzaSy...)
echo.
set /p GEMINI_KEY="Paste your Gemini API key here: "

echo.
echo Step 2: Deploy to Render (FREE)
echo.
echo 1. Go to: https://dashboard.render.com
echo 2. Sign up/Login
echo 3. Click "New +" then "Web Service"
echo 4. Connect this GitHub repo OR use manual deploy
echo.
echo 5. Use these settings:
echo    Name: visionary-backend
echo    Environment: Python 3
echo    Build Command: cd backend ^&^& pip install -r requirements.txt
echo    Start Command: cd backend ^&^& uvicorn main:app --host 0.0.0.0 --port $PORT
echo    Plan: Free
echo.
echo 6. Add Environment Variables:
echo    GEMINI_API_KEY=%GEMINI_KEY%
echo    SECRET_KEY=your-random-32-char-secret-key-here
echo    DATABASE_URL=sqlite+aiosqlite:///./visionary.db
echo.
echo 7. Click "Create Web Service"
echo 8. Wait 5-10 minutes
echo.
echo Your backend will be at: https://visionary-backend.onrender.com
echo.
pause

echo.
echo Step 3: Update Mobile App
echo.
set /p BACKEND_URL="Enter your Render backend URL (e.g., https://visionary-backend.onrender.com): "

echo EXPO_PUBLIC_API_URL=%BACKEND_URL%/api/v1 > mobile_app\.env

echo.
echo Step 4: Build Mobile App
echo.
cd mobile_app
call npm install
call eas build --platform android --profile preview

echo.
echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your app is now using:
echo - Gemini AI (FREE)
echo - Render hosting (FREE)
echo - Real backend integration
echo - NO DEMO MODE
echo.
echo Download APK from: https://expo.dev
echo.
pause
