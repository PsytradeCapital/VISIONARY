@echo off
echo ========================================
echo FIXING MOBILE APP CRASH ISSUE
echo ========================================
echo.

echo Step 1: Mobile app crash fixes applied
echo - Added demo/offline mode
echo - Added error handling for API calls
echo - Prevented crash on backend unavailability
echo - Added connection status indicator
echo.

echo Step 2: Building fixed mobile app...
cd mobile_app

echo.
echo Installing dependencies...
call npm install

echo.
echo Starting Expo development server...
echo.
echo IMPORTANT: The app will now work in DEMO MODE
echo - No backend connection required
echo - Demo data will be displayed
echo - Pull to refresh to try connecting to backend
echo.
echo Press Ctrl+C to stop the server
echo.

call npx expo start

cd ..
