@echo off
echo 🔧 Deploying Backend API Fixes...
echo =====================================

echo Step 1: Navigate to backend directory...
cd backend

echo Step 2: Commit changes to git...
git add .
git commit -m "Fix API endpoints for verification tests"

echo Step 3: Deploy to Railway...
railway up

echo ✅ Backend fixes deployed!
echo 📡 Backend URL: https://visionary-backend-production.up.railway.app
echo 📖 API Docs: https://visionary-backend-production.up.railway.app/docs

pause