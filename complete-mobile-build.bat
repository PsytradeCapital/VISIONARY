@echo off
echo 📱 Completing Mobile App Build...
echo.

cd mobile_app

echo Building Android APK with proper project ID...
eas build --platform android --profile preview

echo.
echo ✅ Mobile app build initiated!
echo.
echo 🔗 Monitor progress at:
echo https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler
echo.
pause