@echo off
echo ========================================
echo Clean Rebuild - Remove Polyfills
echo ========================================
echo.

cd mobile_app

echo Step 1: Backup and replace package.json...
copy package.json package.json.backup
copy package-clean.json package.json

echo.
echo Step 2: Clean install...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

call npm install

echo.
echo Step 3: Building...
call eas build --platform android --profile preview --non-interactive

cd ..
pause
