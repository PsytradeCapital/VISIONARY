@echo off
echo 📱 Creating Fresh Mobile App Project...
echo.

cd mobile_app

echo Step 1: Creating new EAS project...
eas project:init

echo Step 2: Building Android APK...
eas build --platform android --profile preview

echo.
echo ✅ Mobile app created and building!
echo.
echo 📝 What happens next:
echo 1. EAS creates a new project with proper UUID
echo 2. Builds your Android APK (5-10 minutes)
echo 3. Provides download link when ready
echo.
echo 🔗 Monitor progress at: https://expo.dev/
echo.
pause