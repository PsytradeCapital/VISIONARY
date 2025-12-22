@echo off
echo ========================================
echo   BUILDING REAL VISIONARY AI MOBILE APP
echo ========================================
echo.

echo 🧹 Step 1: Cleaning up old attempts...
if exist "visionary_flutter" rmdir /s /q "visionary_flutter"
if exist "visionary_ai_mobile" rmdir /s /q "visionary_ai_mobile"
if exist "flutter_app" rmdir /s /q "flutter_app"

echo.
echo 📱 Step 2: Creating Flutter project...
flutter create visionary_mobile --org com.visionary.ai --project-name visionary_mobile

echo.
echo 📂 Step 3: Copying our real app files...
xcopy /E /Y "mobile\*" "visionary_mobile\"

echo.
echo 📦 Step 4: Installing dependencies...
cd visionary_mobile
flutter pub get

echo.
echo 🔧 Step 5: Configuring Android permissions...
echo ^<uses-permission android:name="android.permission.INTERNET" /^> >> android\app\src\main\AndroidManifest.xml
echo ^<uses-permission android:name="android.permission.RECORD_AUDIO" /^> >> android\app\src\main\AndroidManifest.xml
echo ^<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" /^> >> android\app\src\main\AndroidManifest.xml
echo ^<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" /^> >> android\app\src\main\AndroidManifest.xml

echo.
echo 🚀 Step 6: Building APK...
flutter build apk --release

echo.
echo ========================================
echo   BUILD COMPLETE!
echo ========================================
echo.
echo 📱 APK Location: visionary_mobile\build\app\outputs\flutter-apk\app-release.apk
echo.
echo 📋 To install on phone:
echo 1. Enable Developer Options on your phone
echo 2. Enable USB Debugging
echo 3. Connect phone to computer
echo 4. Run: flutter install
echo.
echo 🔥 Or copy the APK to your phone and install manually!
echo.
pause