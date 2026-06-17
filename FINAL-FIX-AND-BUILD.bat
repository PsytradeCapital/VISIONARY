@echo off
echo ========================================
echo Final Fix - Clean Build
echo ========================================
echo.

cd mobile_app

echo Step 1: Using clean package.json (no problematic polyfills)...
copy /Y package-clean.json package.json

echo.
echo Step 2: Removing old dependencies...
if exist node_modules (
    rmdir /s /q node_modules
)
if exist package-lock.json (
    del package-lock.json
)

echo.
echo Step 3: Installing clean dependencies...
call npm install --legacy-peer-deps

echo.
echo Step 4: Starting build on EAS cloud...
echo (This runs on Expo servers - you can close this window after it starts)
echo.
call eas build --platform android --profile preview --non-interactive

cd ..
echo.
echo ========================================
echo Build submitted to EAS!
echo Check: https://expo.dev
echo ========================================
pause
