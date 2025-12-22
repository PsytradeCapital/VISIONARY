@echo off
echo Building the fresh mobile app...
echo.

REM Change to the fresh mobile directory
cd /d "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh"

echo Current directory: %CD%
echo.

echo Running flutter build apk --debug...
flutter build apk --debug

echo.
echo Build completed! Check the output above for results.
echo If successful, the APK will be in: build\app\outputs\flutter-apk\app-debug.apk
echo.
pause