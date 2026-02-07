@echo off
echo ========================================
echo Fixing Mobile Build - Crypto Error
echo ========================================
echo.

cd mobile_app

echo Step 1: Removing old dependencies...
if exist node_modules rmdir /s /q node_modules
if exist package-lock.json del package-lock.json

echo.
echo Step 2: Installing dependencies with polyfills...
call npm install

echo.
echo Step 3: Installing additional polyfills...
call npm install expo-crypto@~12.4.1 readable-stream@^4.5.2 stream-http@^3.2.0 https-browserify@^1.0.0 url@^0.11.3 path-browserify@^1.0.1 browserify-zlib@^0.2.0 react-native-os@^1.2.6

echo.
echo Step 4: Clearing Expo cache...
call npx expo start --clear

echo.
echo ========================================
echo Dependencies fixed! Now building...
echo ========================================
echo.

echo Building Android APK...
call eas build --platform android --profile preview --non-interactive

echo.
echo ========================================
echo Build process started!
echo ========================================
cd ..
