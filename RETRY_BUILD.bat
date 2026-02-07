@echo off
echo ========================================
echo RETRYING MOBILE BUILD
echo ========================================
echo.

cd mobile_app

echo Building Android APK with fixed configuration...
echo.

call eas build --platform android --profile preview --clear-cache

echo.
echo Build started! Check: https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler/builds
echo.
pause
