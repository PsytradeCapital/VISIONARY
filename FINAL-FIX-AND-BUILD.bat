@echo off
echo ========================================
echo FINAL FIX - Remove Incompatible Packages
echo ========================================
echo.
echo Problem: react-native-os uses deprecated Gradle compile() method
echo Solution: Remove ALL polyfills, let axios use browser build
echo.

cd mobile_app

echo Step 1: Removing incompatible packages...
call npm uninstall browserify-zlib https-browserify path-browserify react-native-os readable-stream stream-http url expo-crypto

echo.
echo Step 2: Clean reinstall...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

call npm install

echo.
echo Step 3: Building APK...
call eas build --platform android --profile preview --non-interactive

echo.
echo ========================================
echo Build Started!
echo ========================================
cd ..
pause
