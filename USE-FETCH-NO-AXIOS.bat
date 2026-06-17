@echo off
echo ========================================
echo Switching to Fetch API (No Axios)
echo ========================================
echo.
echo This will:
echo 1. Replace axios with native fetch
echo 2. Remove axios dependency
echo 3. Build the app
echo.
pause

cd mobile_app

echo.
echo Step 1: Backing up old API service...
if exist src\services\api.ts (
    copy src\services\api.ts src\services\api-axios-backup.ts
    echo Backup created!
) else (
    echo No existing api.ts found, skipping backup
)

echo.
echo Step 2: Replacing with fetch-based API...
if exist src\services\api-fetch.ts (
    copy /Y src\services\api-fetch.ts src\services\api.ts
    echo API service replaced with fetch version!
) else (
    echo ERROR: api-fetch.ts not found!
    cd ..
    pause
    exit /b 1
)

echo.
echo Step 3: Removing axios from package.json...
call npm uninstall axios
echo Axios removed!

echo.
echo Step 4: Clean install...
if exist node_modules\axios (
    rmdir /s /q node_modules\axios
    echo Axios folder removed!
)

echo.
echo Step 5: Starting build on EAS...
echo This will take 10-15 minutes on cloud servers.
echo You can close this window after build starts.
echo.
call eas build --platform android --profile preview --non-interactive

cd ..
echo.
echo ========================================
echo Build process completed!
echo Check: https://expo.dev
echo ========================================
pause
