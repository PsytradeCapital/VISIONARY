@echo off
echo ========================================
echo Building Android APK with Fixed Dependencies
echo ========================================
echo.

cd mobile_app

echo Starting EAS Build...
echo This will take 10-15 minutes on the cloud.
echo.

call eas build --platform android --profile preview --non-interactive

echo.
echo ========================================
echo Build submitted! Check EAS dashboard for progress.
echo ========================================
echo.

cd ..
pause
