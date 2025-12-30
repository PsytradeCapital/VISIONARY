@echo off
echo 🔧 Fixing App Crash Issues...
echo ================================

echo Step 1: Navigate to mobile app directory...
cd mobile_app

echo Step 2: Clear Metro cache...
npx expo start --clear

echo Step 3: Build fixed APK...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ App crash fixes applied!
echo.
echo 🔧 Fixes Applied:
echo   • Added Error Boundary to catch crashes
echo   • Fixed AsyncStorage error handling
echo   • Graceful fallbacks for theme context
echo   • Better error logging
echo.
echo 📱 The new build should open properly without crashing!
echo.
pause