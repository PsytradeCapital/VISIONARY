@echo off
echo 📱 Building Visionary AI Mobile App
echo.

echo Current directory: %CD%
echo.

REM Check if we're in the right directory
if exist mobile (
    echo ✅ Found mobile folder
    cd mobile
) else if exist ..\mobile (
    echo ✅ Found mobile folder in parent directory
    cd ..\mobile
) else if exist ..\..\mobile (
    echo ✅ Found mobile folder two levels up
    cd ..\..\mobile
) else (
    echo ❌ Cannot find mobile folder
    echo Please run this from VISIONARY directory
    pause
    exit /b 1
)

echo.
echo 📂 Now in: %CD%
echo.

echo Step 1: Cleaning Flutter project...
flutter clean

echo.
echo Step 2: Getting dependencies...
flutter pub get

echo.
echo Step 3: Building APK (this takes 10-15 minutes)...
flutter build apk --release

echo.
if exist build\app\outputs\flutter-apk\app-release.apk (
    echo.
    echo ✅✅✅ SUCCESS! ✅✅✅
    echo.
    echo 📱 Your APK is ready!
    echo 📂 Location: %CD%\build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo 📲 To install on your phone:
    echo 1. Copy app-release.apk to your phone
    echo 2. Enable "Install from unknown sources"
    echo 3. Tap the APK to install
    echo.
    echo Opening APK folder...
    start explorer build\app\outputs\flutter-apk\
) else (
    echo.
    echo ❌ Build failed
    echo Check the errors above
)

echo.
pause