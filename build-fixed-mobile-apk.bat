@echo off
echo ========================================
echo BUILDING FIXED MOBILE APK
echo ========================================
echo.

echo This will build an APK with crash fixes:
echo - Demo mode enabled by default
echo - No crash on backend unavailability
echo - Offline functionality
echo - Pull to refresh for backend connection
echo.

cd mobile_app

echo Step 1: Installing dependencies...
call npm install

echo.
echo Step 2: Building Android APK with EAS...
echo This will take 5-10 minutes...
echo.

call eas build --platform android --profile preview

echo.
echo ========================================
echo BUILD COMPLETE!
echo ========================================
echo.
echo The APK will be available at:
echo https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler/builds
echo.
echo Download and install on your phone to test!
echo.

cd ..
pause
