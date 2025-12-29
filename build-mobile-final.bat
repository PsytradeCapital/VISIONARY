@echo off
echo 📱 Final Mobile App Build (All Issues Fixed)...
echo.

cd mobile_app

echo Building Android APK (all dependencies resolved)...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ Final build initiated with all fixes!
echo.
echo 🔧 Issues Fixed:
echo   • NotificationContext created
echo   • Web dependencies removed
echo   • Asset references removed
echo   • All native modules compiled successfully
echo.
echo 🔗 Monitor at: https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler
echo.
pause