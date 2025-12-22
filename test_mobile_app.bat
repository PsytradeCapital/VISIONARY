@echo off
echo 🧪 Testing Visionary AI Mobile App
echo.

cd visionary_mobile

echo 📋 Checking Flutter project...
flutter doctor

echo.
echo 🔍 Analyzing code...
flutter analyze

echo.
echo 🚀 Running app in debug mode...
echo (This will open the app in an emulator or connected device)
echo.
flutter run

pause