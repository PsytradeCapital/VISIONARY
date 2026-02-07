@echo off
echo ========================================
echo Fixing Gradle Build Error
echo ========================================
echo.

cd mobile_app

echo Removing problematic polyfills...
call npm uninstall browserify-zlib https-browserify path-browserify react-native-os readable-stream stream-http url expo-crypto

echo.
echo Cleaning build cache...
if exist android\app\build rmdir /s /q android\app\build
if exist android\build rmdir /s /q android\build

echo.
echo Dependencies cleaned! Metro config will force axios to use browser version.
echo.
echo Now building...
call eas build --platform android --profile preview --non-interactive

cd ..
pause
