@echo off
echo ========================================
echo Forcing Axios Browser Build
echo ========================================
echo.

cd mobile_app

echo Step 1: Applying fixed package.json...
copy /Y package-clean.json package.json

echo.
echo Step 2: Clean reinstall...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

call npm install

echo.
echo Step 3: Building with browser axios...
call eas build --platform android --profile preview --non-interactive

cd ..
echo.
echo Build started! Check: https://expo.dev
pause
