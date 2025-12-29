@echo off
echo 📱 Final Mobile App Build (Fixed Web Issue)...
echo.

cd mobile_app

echo Building Android APK (web support removed)...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ Final build initiated!
echo.
echo 🔗 Monitor at: https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler
echo.
pause