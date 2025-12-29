@echo off
echo 📱 Direct Mobile App Build...
echo.

cd mobile_app

echo Building Android APK now...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ Build initiated!
echo Monitor at: https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler
echo.
pause