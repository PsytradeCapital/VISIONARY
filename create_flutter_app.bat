@echo off
echo 🚀 Creating Visionary AI Flutter App
echo.

echo � SStep 1: Finding Flutter installation...

REM Check common Flutter locations
set "FLUTTER_CMD="
if exist "C:\flutter\bin\flutter.exe" set "FLUTTER_CMD=C:\flutter\bin\flutter.exe"
if exist "C:\src\flutter\bin\flutter.exe" set "FLUTTER_CMD=C:\src\flutter\bin\flutter.exe"
if exist "%USERPROFILE%\flutter\bin\flutter.exe" set "FLUTTER_CMD=%USERPROFILE%\flutter\bin\flutter.exe"
if exist "%USERPROFILE%\Downloads\flutter\bin\flutter.exe" set "FLUTTER_CMD=%USERPROFILE%\Downloads\flutter\bin\flutter.exe"
if exist "C:\Program Files\flutter\bin\flutter.exe" set "FLUTTER_CMD=C:\Program Files\flutter\bin\flutter.exe"
if exist "%LOCALAPPDATA%\flutter\bin\flutter.exe" set "FLUTTER_CMD=%LOCALAPPDATA%\flutter\bin\flutter.exe"

REM Try to find flutter in PATH
if "%FLUTTER_CMD%"=="" (
    echo 🔍 Searching for Flutter in system...
    for %%i in (flutter.exe) do set "FLUTTER_CMD=%%~$PATH:i"
)

if "%FLUTTER_CMD%"=="" (
    echo ❌ Flutter not found! Please install Flutter or add it to PATH
    echo 📝 Download from: https://flutter.dev/docs/get-started/install/windows
    pause
    exit /b 1
)

echo ✅ Found Flutter at: %FLUTTER_CMD%
echo.

echo 📱 Step 2: Creating Flutter project...
"%FLUTTER_CMD%" create visionary_flutter
cd visionary_flutter

echo 📦 Step 3: Adding dependencies...
"%FLUTTER_CMD%" pub add http
"%FLUTTER_CMD%" pub add dio
"%FLUTTER_CMD%" pub add provider
"%FLUTTER_CMD%" pub add go_router
"%FLUTTER_CMD%" pub add file_picker
"%FLUTTER_CMD%" pub add image_picker
"%FLUTTER_CMD%" pub add shared_preferences
"%FLUTTER_CMD%" pub add path_provider

echo 🎨 Step 3: Project created successfully!
echo.
echo 📱 Next steps:
echo 1. I'll create all the screens (Dashboard, Schedule, Upload, Progress)
echo 2. Add your gradient designs and animations
echo 3. Use your blue eye icon
echo 4. Connect to your Python backend
echo 5. Build APK for easy installation
echo.
echo 🚀 Ready to build your mobile app!
pause