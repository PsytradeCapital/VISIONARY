@echo off
echo 📱 Manual Mobile App Build (if needed)...
echo.

cd mobile_app

echo Building Android APK...
eas build --platform android --profile preview

echo.
echo ✅ Build initiated!
echo Monitor progress at: https://expo.dev/accounts/martinmbugua300/projects/visionary-mobile/builds
echo.
pause