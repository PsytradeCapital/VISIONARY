@echo off
echo 🔧 Fixing Flutter PATH...
echo.

echo 📍 Checking common Flutter installation locations...
if exist "C:\flutter\bin\flutter.exe" (
    echo ✅ Found Flutter at: C:\flutter\bin\
    set "FLUTTER_PATH=C:\flutter\bin"
    goto :found
)

if exist "C:\src\flutter\bin\flutter.exe" (
    echo ✅ Found Flutter at: C:\src\flutter\bin\
    set "FLUTTER_PATH=C:\src\flutter\bin"
    goto :found
)

if exist "%USERPROFILE%\flutter\bin\flutter.exe" (
    echo ✅ Found Flutter at: %USERPROFILE%\flutter\bin\
    set "FLUTTER_PATH=%USERPROFILE%\flutter\bin"
    goto :found
)

echo ❌ Flutter not found in common locations.
echo 📝 Please check where Flutter is installed:
echo    - Look for flutter folder on your C: drive
echo    - Or run: where flutter
echo.
pause
exit /b 1

:found
echo.
echo 🚀 Adding Flutter to PATH for this session...
set "PATH=%FLUTTER_PATH%;%PATH%"

echo ✅ Testing Flutter...
flutter --version

echo.
echo 🎯 Flutter is now ready! Creating your app...
echo.

echo 📱 Creating Visionary AI Flutter App...
flutter create visionary_ai_mobile --org com.visionary.ai --project-name visionary_ai_mobile

echo.
echo ✅ Flutter app created successfully!
echo 📂 Location: visionary_ai_mobile\
echo.
echo 🔥 Next: I'll customize it with your designs!
pause