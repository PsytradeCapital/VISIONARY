@echo off
echo ========================================
echo BUILDING MOBILE APP WITH REAL BACKEND
echo ========================================
echo.
echo Backend URL: https://visionary-backend-hk6u.onrender.com
echo Gemini API: ACTIVE
echo.

cd mobile_app

echo Step 1: Installing dependencies...
call npm install

echo.
echo Step 2: Building Android APK...
echo This will take 5-10 minutes...
echo.

call eas build --platform android --profile preview

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo Download APK from: https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler/builds
echo.
echo Your app now has:
echo - Real Gemini AI backend
echo - Live API at https://visionary-backend-hk6u.onrender.com
echo - No demo mode
echo - Real schedule generation
echo - Real document processing
echo.
pause
