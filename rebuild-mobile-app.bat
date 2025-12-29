@echo off
echo 📱 Rebuilding Mobile App (Fixed)...
echo.

cd mobile_app

echo Step 1: Fixing assets and dependencies...
call ..\fix-mobile-assets.bat

echo Step 2: Building Android APK with fixes...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ Mobile app rebuild initiated!
echo.
echo 🔗 Monitor progress at:
echo https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler
echo.
pause