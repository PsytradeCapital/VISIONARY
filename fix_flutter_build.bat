@echo off
echo 🔧 Fixing Flutter Build Issues...
echo.

echo Step 1: Cleaning Flutter project...
flutter clean

echo.
echo Step 2: Getting dependencies...
flutter pub get

echo.
echo Step 3: Updating Gradle wrapper...
cd android
gradlew wrapper --gradle-version=7.6.3
cd ..

echo.
echo Step 4: Trying build again...
flutter build apk --release

echo.
echo ✅ Build should work now!
pause