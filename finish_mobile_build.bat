@echo off
echo 📱 Finishing Mobile App Build
echo.

echo Current directory: %CD%
echo.

REM Go to VISIONARY directory first
if exist VISIONARY (
    cd VISIONARY
    echo ✅ Found VISIONARY directory
) else (
    echo ❌ Cannot find VISIONARY directory
    echo Please run this from Desktop
    pause
    exit /b 1
)

echo.
echo Step 1: Copying your code to fresh project...
if exist mobile (
    echo ✅ Found original mobile folder
    xcopy mobile\lib visionary_mobile_fresh\lib /E /Y
    xcopy mobile\assets visionary_mobile_fresh\assets /E /Y 2>nul
    copy mobile\pubspec.yaml visionary_mobile_fresh\pubspec.yaml /Y
) else (
    echo ❌ Original mobile folder not found
)

echo.
echo Step 2: Going to fresh project...
cd visionary_mobile_fresh

echo.
echo Step 3: Getting dependencies...
flutter pub get

echo.
echo Step 4: Building APK...
flutter build apk --release

echo.
if exist build\app\outputs\flutter-apk\app-release.apk (
    echo.
    echo ✅✅✅ SUCCESS! APK BUILT! ✅✅✅
    echo.
    echo 📱 Your APK is ready at:
    echo %CD%\build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo 📲 Copy this file to your phone and install it!
    echo.
    echo Opening APK folder...
    start explorer build\app\outputs\flutter-apk\
) else (
    echo ❌ Release build failed, trying debug build...
    flutter build apk --debug
    if exist build\app\outputs\flutter-apk\app-debug.apk (
        echo ✅ Debug APK created!
        echo Location: %CD%\build\app\outputs\flutter-apk\app-debug.apk
        start explorer build\app\outputs\flutter-apk\
    )
)

echo.
pause