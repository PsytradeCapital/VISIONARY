@echo off
echo 📱 Rebuilding Mobile App with Proper Icon...
echo =============================================

echo Step 1: Navigate to mobile app directory...
cd mobile_app

echo Step 2: Clear Expo cache...
npx expo install --fix

echo Step 3: Build Android APK with new icon...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ Mobile app rebuild initiated with proper icon!
echo.
echo 🎨 Icon Updates Applied:
echo   • Copied appicon.png to mobile_app/assets/icon.png
echo   • Updated app.json with icon and splash screen
echo   • Added proper app name: "Visionary AI Scheduler"
echo.
echo 🔗 Monitor build at: https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler
echo.
echo 📱 The new APK will have the proper Visionary logo!
echo.
pause