@echo off
echo 🔧 Fixing Mobile Build Issues
echo.

cd mobile

echo Step 1: Updating Gradle wrapper...
cd android
if exist gradlew.bat (
    gradlew wrapper --gradle-version=7.6.3
) else (
    echo Gradle wrapper not found, continuing...
)
cd ..

echo.
echo Step 2: Cleaning everything...
flutter clean
rmdir /s /q build 2>nul
rmdir /s /q .dart_tool 2>nul

echo.
echo Step 3: Getting fresh dependencies...
flutter pub get

echo.
echo Step 4: Checking for Flutter doctor issues...
flutter doctor

echo.
echo Step 5: Building APK with verbose output...
flutter build apk --release --verbose

echo.
pause