@echo off
echo 📱 Building Visionary AI Mobile App for Phone
echo.

echo Step 1: Going to mobile directory...
cd mobile

echo.
echo Step 2: Checking Flutter project...
if exist pubspec.yaml (
    echo ✅ Flutter project found
) else (
    echo ❌ No Flutter project found
    pause
    exit /b 1
)

echo.
echo Step 3: Cleaning project...
flutter clean

echo.
echo Step 4: Getting dependencies...
flutter pub get

echo.
echo Step 5: Building APK for phone...
echo This may take 10-15 minutes...
flutter build apk --release

echo.
if exist build\app\outputs\flutter-apk\app-release.apk (
    echo ✅ SUCCESS! APK built successfully!
    echo.
    echo 📱 APK Location: mobile\build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo 📲 To install on phone:
    echo 1. Copy app-release.apk to your phone
    echo 2. Enable "Install from unknown sources" in phone settings
    echo 3. Tap the APK file to install
    echo.
    echo Opening APK folder...
    explorer build\app\outputs\flutter-apk\
) else (
    echo ❌ Build failed. Check errors above.
)

echo.
pause