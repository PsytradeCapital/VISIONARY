@echo off
echo 🔧 Building Crash-Fixed APK...
echo ===============================

echo Step 1: Navigate to mobile app directory...
cd mobile_app

echo Step 2: Stop Metro server (if running)...
taskkill /f /im node.exe 2>nul

echo Step 3: Build standalone APK with crash fixes...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ Building crash-fixed APK!
echo.
echo 🔧 Crash Fixes Included:
echo   • Error Boundary to prevent crashes
echo   • Fixed AsyncStorage handling
echo   • Graceful theme context fallbacks
echo   • Better error logging
echo.
echo 📱 This will create a standalone APK that doesn't need Expo Go!
echo.
pause