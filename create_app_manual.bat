@echo off
echo 🚀 Visionary AI - Manual Flutter App Creation
echo.
echo Since Flutter is installed but not in PATH, let's create the app manually.
echo.

echo Please follow these steps:
echo.
echo 1️⃣ Open a new Command Prompt or PowerShell
echo 2️⃣ Navigate to your Flutter installation directory
echo 3️⃣ Run these commands:
echo.
echo    cd bin
echo    flutter create visionary_ai_mobile --org com.visionary.ai
echo    cd visionary_ai_mobile
echo    flutter pub add http dio provider go_router file_picker image_picker shared_preferences path_provider
echo.
echo 4️⃣ Then run: flutter run
echo.
echo 💡 OR - Add Flutter to your PATH permanently:
echo    - Find your Flutter folder (probably C:\flutter or similar)
echo    - Add C:\flutter\bin to your Windows PATH environment variable
echo    - Restart this terminal
echo    - Then run: create_flutter_app.bat
echo.
echo 🔍 To find Flutter location, check these folders:
echo    - C:\flutter
echo    - C:\src\flutter
echo    - %USERPROFILE%\flutter
echo    - %USERPROFILE%\Downloads\flutter
echo.

pause

echo.
echo 🎨 Meanwhile, I'll create the Flutter app structure for you...
echo.

REM Create the basic app structure
mkdir visionary_ai_mobile 2>nul
cd visionary_ai_mobile

mkdir lib 2>nul
mkdir lib\screens 2>nul
mkdir lib\services 2>nul
mkdir lib\models 2>nul
mkdir lib\widgets 2>nul

echo Creating Flutter app files...

REM Create pubspec.yaml
echo name: visionary_ai_mobile > pubspec.yaml
echo description: AI-powered personal scheduler mobile app >> pubspec.yaml
echo version: 1.0.0+1 >> pubspec.yaml
echo. >> pubspec.yaml
echo environment: >> pubspec.yaml
echo   sdk: '>=3.0.0 <4.0.0' >> pubspec.yaml
echo. >> pubspec.yaml
echo dependencies: >> pubspec.yaml
echo   flutter: >> pubspec.yaml
echo     sdk: flutter >> pubspec.yaml
echo   http: ^1.1.0 >> pubspec.yaml
echo   dio: ^5.3.2 >> pubspec.yaml
echo   provider: ^6.0.5 >> pubspec.yaml
echo   go_router: ^12.1.1 >> pubspec.yaml
echo   file_picker: ^6.1.1 >> pubspec.yaml
echo   image_picker: ^1.0.4 >> pubspec.yaml
echo   shared_preferences: ^2.2.2 >> pubspec.yaml
echo   path_provider: ^2.1.1 >> pubspec.yaml
echo. >> pubspec.yaml
echo dev_dependencies: >> pubspec.yaml
echo   flutter_test: >> pubspec.yaml
echo     sdk: flutter >> pubspec.yaml
echo   flutter_lints: ^3.0.0 >> pubspec.yaml
echo. >> pubspec.yaml
echo flutter: >> pubspec.yaml
echo   uses-material-design: true >> pubspec.yaml

echo ✅ Created pubspec.yaml
echo ✅ Created folder structure
echo.
echo 📱 Next: Run Flutter commands in your Flutter bin directory!
echo.
pause