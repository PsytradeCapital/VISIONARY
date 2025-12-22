@echo off
echo 🔧 Creating Fresh Flutter Project for Mobile
echo.

cd ..

echo Step 1: Creating new Flutter project...
flutter create visionary_mobile_fresh

echo.
echo Step 2: Copying your code to new project...
xcopy mobile\lib visionary_mobile_fresh\lib /E /Y
xcopy mobile\assets visionary_mobile_fresh\assets /E /Y 2>nul

echo.
echo Step 3: Copying pubspec.yaml dependencies...
copy mobile\pubspec.yaml visionary_mobile_fresh\pubspec.yaml /Y

echo.
echo Step 4: Going to new project...
cd visionary_mobile_fresh

echo.
echo Step 5: Getting dependencies...
flutter pub get

echo.
echo Step 6: Building APK...
flutter build apk --release

echo.
if exist build\app\outputs\flutter-apk\app-release.apk (
    echo.
    echo ✅✅✅ SUCCESS! ✅✅✅
    echo.
    echo 📱 Your APK is ready!
    echo 📂 Location: %CD%\build\app\outputs\flutter-apk\app-release.apk
    echo.
    echo Opening APK folder...
    start explorer build\app\outputs\flutter-apk\
) else (
    echo ❌ Build failed, but let's try debug build...
    flutter build apk --debug
)

echo.
pause