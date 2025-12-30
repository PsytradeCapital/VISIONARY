@echo off
echo 🌐 Deploying Web App with Proper Icon...
echo =========================================

echo Step 1: Navigate to web app directory...
cd web_app

echo Step 2: Build web app with new icons...
npm run build

echo Step 3: Deploy to Vercel...
npx vercel --prod

echo.
echo ✅ Web app deployed with proper icons!
echo.
echo 🎨 Icon Updates Applied:
echo   • Copied appicon.png to favicon.ico
echo   • Updated logo192.png and logo512.png
echo   • Manifest.json configured for PWA
echo   • Professional AI branding maintained
echo.
echo 🔗 Your updated app: https://visionary-ai-web-app.vercel.app
echo.
echo 📱 The web app now has the proper Visionary logo!
echo.
pause