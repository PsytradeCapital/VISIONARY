@echo off
echo 🚀 Visionary AI - Flutter Setup & App Creation
echo.

REM First, let's try to use Flutter if it's already working
echo Testing if Flutter is available...
flutter --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Flutter is working! Creating your app...
    goto :create_visionary_app
)

echo 📥 Flutter not in PATH. Let's set it up properly...
echo.

REM Check if Flutter is already downloaded somewhere
set "FLUTTER_FOUND="
for %%d in (
    "C:\flutter\bin"
    "C:\src\flutter\bin"
    "%USERPROFILE%\flutter\bin"
    "%USERPROFILE%\Downloads\flutter\bin"
    "%USERPROFILE%\Desktop\flutter\bin"
    "%LOCALAPPDATA%\flutter\bin"
) do (
    if exist "%%d\flutter.exe" (
        echo ✅ Found Flutter at: %%d
        set "FLUTTER_FOUND=%%d"
        goto :found_flutter
    )
)

echo ❌ Flutter not found in common locations
echo.
echo 🔧 Quick Fix Options:
echo 1. Download Flutter automatically
echo 2. I'll tell you where my Flutter is installed
echo 3. Install via Chocolatey (if you have it)
echo.
choice /c 123 /m "Choose option"

if errorlevel 3 goto :choco_install
if errorlevel 2 goto :manual_path
if errorlevel 1 goto :auto_download

:auto_download
echo.
echo 📥 Downloading Flutter...
echo Opening download page - please download and extract to C:\flutter
start https://docs.flutter.dev/get-started/install/windows
echo.
echo After downloading:
echo 1. Extract the zip file to C:\flutter
echo 2. Run this script again
pause
exit /b 0

:choco_install
echo.
echo 📦 Installing Flutter via Chocolatey...
choco install flutter
if %errorlevel% equ 0 (
    echo ✅ Flutter installed! Refreshing environment...
    refreshenv
    goto :create_visionary_app
) else (
    echo ❌ Chocolatey install failed. Try manual download.
    pause
    exit /b 1
)

:manual_path
echo.
set /p user_flutter_path="Enter your Flutter installation path (e.g., C:\flutter): "
if exist "%user_flutter_path%\bin\flutter.exe" (
    set "FLUTTER_FOUND=%user_flutter_path%\bin"
    goto :found_flutter
) else (
    echo ❌ Flutter not found at: %user_flutter_path%
    pause
    exit /b 1
)

:found_flutter
echo.
echo 🔧 Adding Flutter to PATH for this session...
set "PATH=%FLUTTER_FOUND%;%PATH%"
echo ✅ Flutter ready!

:create_visionary_app
echo.
echo 🎨 Creating Visionary AI Mobile App...
echo.

REM Create the Flutter app
if defined FLUTTER_FOUND (
    "%FLUTTER_FOUND%\flutter.exe" create visionary_ai_mobile --org com.visionary.ai
) else (
    flutter create visionary_ai_mobile --org com.visionary.ai
)

if %errorlevel% neq 0 (
    echo ❌ Failed to create Flutter app
    pause
    exit /b 1
)

cd visionary_ai_mobile

echo.
echo 📦 Adding essential packages...
if defined FLUTTER_FOUND (
    "%FLUTTER_FOUND%\flutter.exe" pub add http dio provider go_router file_picker image_picker shared_preferences path_provider
) else (
    flutter pub add http dio provider go_router file_picker image_picker shared_preferences path_provider
)

echo.
echo 🎉 SUCCESS! Visionary AI Mobile App Created!
echo.
echo 📂 Location: %cd%
echo.
echo 🚀 Next steps:
echo 1. Connect your phone or start an emulator
echo 2. Run: flutter run
echo.
echo 💡 I'll now create the custom screens for your AI scheduler!
pause