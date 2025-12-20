@echo off
echo 🚀 Simple Flutter Setup for Visionary AI
echo.

echo Let's try to find Flutter step by step...
echo.

echo 1. Trying flutter command directly...
flutter --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ Flutter found in PATH!
    goto :create_app
)

echo 2. Checking if you have Flutter SDK downloaded...
echo Please tell me where you installed Flutter:
echo Common locations:
echo   - C:\flutter
echo   - C:\src\flutter  
echo   - %USERPROFILE%\flutter
echo   - Downloaded but not extracted?
echo.

set /p flutter_path="Enter Flutter path (or press Enter to download): "

if "%flutter_path%"=="" (
    echo.
    echo 📥 Let's download Flutter for you...
    echo Opening Flutter download page...
    start https://flutter.dev/docs/get-started/install/windows
    echo.
    echo After downloading:
    echo 1. Extract to C:\flutter
    echo 2. Add C:\flutter\bin to your PATH
    echo 3. Run this script again
    pause
    exit /b 0
)

if exist "%flutter_path%\bin\flutter.exe" (
    echo ✅ Found Flutter at: %flutter_path%
    set "FLUTTER_CMD=%flutter_path%\bin\flutter.exe"
    goto :create_app
) else (
    echo ❌ Flutter not found at: %flutter_path%
    echo Please check the path and try again
    pause
    exit /b 1
)

:create_app
echo.
echo 🎯 Creating Visionary AI Flutter App...
if defined FLUTTER_CMD (
    "%FLUTTER_CMD%" create visionary_ai_app
) else (
    flutter create visionary_ai_app
)

echo.
echo ✅ App created! Next steps:
echo 1. cd visionary_ai_app
echo 2. flutter run
echo.
pause