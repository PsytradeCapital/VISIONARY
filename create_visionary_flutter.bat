@echo off
echo 📱 Creating Visionary AI Flutter App
echo.

REM Try to find Flutter
set "FLUTTER_FOUND=0"

if exist "C:\flutter\bin\flutter.exe" (
    set "PATH=C:\flutter\bin;%PATH%"
    set "FLUTTER_FOUND=1"
)

if exist "C:\src\flutter\bin\flutter.exe" (
    set "PATH=C:\src\flutter\bin;%PATH%"
    set "FLUTTER_FOUND=1"
)

if exist "%USERPROFILE%\flutter\bin\flutter.exe" (
    set "PATH=%USERPROFILE%\flutter\bin;%PATH%"
    set "FLUTTER_FOUND=1"
)

if "%FLUTTER_FOUND%"=="0" (
    echo ❌ Flutter not found. Let me help you find it...
    echo.
    echo 🔍 Please run this command to find Flutter:
    echo    dir C:\ /s /b flutter.exe
    echo.
    echo 📝 Then add the folder containing flutter.exe to your PATH
    echo    Example: C:\flutter\bin
    echo.
    pause
    exit /b 1
)

echo ✅ Flutter found! Creating app...
echo.

REM Create Flutter project
flutter create visionary_ai_mobile --org com.visionary.ai --project-name visionary_ai_mobile

if errorlevel 1 (
    echo ❌ Failed to create Flutter project
    echo 💡 Try running: flutter doctor
    pause
    exit /b 1
)

echo.
echo 🎉 Flutter app created successfully!
echo 📂 Project location: visionary_ai_mobile\
echo.
echo 🔥 Next steps:
echo 1. I'll customize the app with your designs
echo 2. Add your blue eye icon
echo 3. Create all screens (Dashboard, Schedule, Upload, Progress)
echo 4. Connect to your Python backend
echo 5. Build APK for installation
echo.
pause