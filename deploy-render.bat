@echo off
echo ========================================
echo DEPLOYING TO RENDER (FREE HOSTING)
echo ========================================
echo.

echo Step 1: Install Render CLI
npm install -g render-cli

echo.
echo Step 2: Login to Render
echo Visit: https://dashboard.render.com
echo Create account if you don't have one
echo.
pause

echo.
echo Step 3: Create new Web Service
echo 1. Go to https://dashboard.render.com/select-repo
echo 2. Connect your GitHub repository
echo 3. Or use "Deploy from Git URL"
echo 4. Set these values:
echo    - Name: visionary-backend
echo    - Environment: Python
echo    - Build Command: cd backend ^&^& pip install -r requirements.txt
echo    - Start Command: cd backend ^&^& uvicorn main:app --host 0.0.0.0 --port $PORT
echo    - Plan: Free
echo.
echo 5. Add Environment Variables:
echo    - DATABASE_URL: sqlite+aiosqlite:///./visionary.db
echo    - SECRET_KEY: (generate random 32+ chars)
echo    - GEMINI_API_KEY: (get from https://makersuite.google.com/app/apikey)
echo.
echo 6. Click "Create Web Service"
echo.
echo Your backend will be live at: https://visionary-backend.onrender.com
echo.
pause
