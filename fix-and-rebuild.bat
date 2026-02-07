@echo off
echo Fixing Mobile Build - Installing Polyfills
echo.

cd mobile_app

echo Cleaning old files...
if exist node_modules (
    echo Removing node_modules...
    rmdir /s /q node_modules
)
if exist package-lock.json (
    del package-lock.json
)

echo.
echo Installing all dependencies...
call npm install

echo.
echo Build fixed! Now you can run:
echo   cd mobile_app
echo   eas build --platform android --profile preview
echo.

cd ..
pause
