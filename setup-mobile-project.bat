@echo off
echo 📱 Setting up Mobile Project Properly...
echo.

cd mobile_app

echo Step 1: Initialize EAS project...
eas project:init

echo Step 2: Configure project...
eas build:configure

echo Step 3: Building Android APK...
eas build --platform android --profile preview

echo.
echo ✅ Mobile app setup and build complete!
echo.
pause