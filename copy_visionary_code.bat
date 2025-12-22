@echo off
echo 🔄 Copying Visionary AI Code to Working Flutter Project
echo.

echo Current directory: %CD%
echo.

REM Check if we're in the right place
if exist lib\main.dart (
    echo ✅ Found Flutter project
) else (
    echo ❌ Not in Flutter project directory
    echo Please run from: visionary_mobile_fresh
    pause
    exit /b 1
)

echo.
echo Step 1: Backing up original files...
if not exist backup mkdir backup
copy lib\main.dart backup\main.dart.original

echo.
echo Step 2: Copying Visionary AI code...
if exist ..\VISIONARY\mobile\lib (
    echo ✅ Found Visionary mobile code
    xcopy ..\VISIONARY\mobile\lib lib /E /Y
    xcopy ..\VISIONARY\mobile\assets assets /E /Y 2>nul
    copy ..\VISIONARY\mobile\pubspec.yaml pubspec.yaml /Y
) else (
    echo ❌ Cannot find Visionary mobile code
    echo Looking for: ..\VISIONARY\mobile\lib
    pause
    exit /b 1
)

echo.
echo Step 3: Getting new dependencies...
flutter pub get

echo.
echo Step 4: Building new APK with Visionary AI...
flutter build apk --release

echo.
if exist build\app\outputs\flutter-apk\app-release.apk (
    echo ✅✅✅ SUCCESS! VISIONARY AI APK READY! ✅✅✅
    echo.
    echo 📱 Your Visionary AI APK: build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo Opening APK folder...
    start explorer build\app\outputs\flutter-apk\
) else (
    echo ❌ Build failed
)

echo.
pause