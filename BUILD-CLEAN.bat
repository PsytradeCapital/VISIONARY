@echo off
echo ========================================
echo Building with Clean Dependencies
echo ========================================
echo.
echo All problematic packages removed!
echo Building APK now...
echo.

cd mobile_app
call eas build --platform android --profile preview --non-interactive

cd ..
echo.
echo Build submitted!
pause
