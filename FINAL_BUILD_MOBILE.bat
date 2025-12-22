@echo off
echo ========================================
echo   FINAL BUILD - REAL VISIONARY AI MOBILE
echo ========================================
echo.

echo 🧹 Cleaning workspace...
if exist "visionary_mobile" rmdir /s /q "visionary_mobile"

echo.
echo 📱 Creating Flutter project...
flutter create visionary_mobile --org com.visionary.ai --project-name visionary_mobile

echo.
echo 📂 Setting up project structure...
cd visionary_mobile

echo.
echo 📝 Copying pubspec.yaml...
copy "..\mobile\pubspec.yaml" "pubspec.yaml"

echo.
echo 📦 Getting dependencies...
flutter pub get

echo.
echo 📱 Copying app files...
xcopy /E /Y "..\mobile\lib\*" "lib\"

echo.
echo 🔧 Configuring Android permissions...
echo ^<uses-permission android:name="android.permission.INTERNET" /^> >> android\app\src\main\AndroidManifest.xml
echo ^<uses-permission android:name="android.permission.RECORD_AUDIO" /^> >> android\app\src\main\AndroidManifest.xml
echo ^<uses-permission android:name="android.permission.CAMERA" /^> >> android\app\src\main\AndroidManifest.xml
echo ^<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" /^> >> android\app\src\main\AndroidManifest.xml
echo ^<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" /^> >> android\app\src\main\AndroidManifest.xml

echo.
echo 🚀 Building APK...
flutter build apk --release

echo.
echo ========================================
echo   🎉 BUILD COMPLETE!
echo ========================================
echo.
echo 📱 APK Location: visionary_mobile\build\app\outputs\flutter-apk\app-release.apk
echo 📂 Project Location: visionary_mobile\
echo.
echo 🔥 FEATURES INCLUDED:
echo ✅ Real authentication (login/register)
echo ✅ Voice recording with microphone
echo ✅ Document upload (PDF, DOC, TXT)
echo ✅ Photo upload from camera/gallery
echo ✅ Text input processing
echo ✅ Connected to your backend API
echo ✅ Beautiful gradient UI matching web app
echo ✅ Bottom navigation with 4 screens
echo ✅ Dashboard with real user data
echo.
echo 📋 TO INSTALL ON PHONE:
echo 1. Enable Developer Options
echo 2. Enable USB Debugging
echo 3. Connect phone via USB
echo 4. Run: flutter install
echo.
echo 📱 OR copy APK to phone and install manually!
echo.
echo 🌐 BACKEND CONNECTION:
echo - Make sure your backend is running on http://localhost:8000
echo - For real device, update API URL in lib/services/api_service.dart
echo.
pause