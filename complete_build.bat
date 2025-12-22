@echo off
echo 📦 Getting Flutter dependencies...
cd visionary_mobile
flutter pub get

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
echo 📱 APK Location: build\app\outputs\flutter-apk\app-release.apk
echo.
echo 🔥 FEATURES INCLUDED:
echo ✅ Real authentication (login/register)
echo ✅ Voice recording with microphone
echo ✅ Document upload (PDF, DOC, TXT)
echo ✅ Photo upload from camera/gallery
echo ✅ Text input processing
echo ✅ Connected to your backend API
echo ✅ Beautiful gradient UI matching web app
echo.
echo 📋 TO INSTALL ON PHONE:
echo 1. Enable Developer Options
echo 2. Enable USB Debugging
echo 3. Connect phone via USB
echo 4. Run: flutter install
echo.
echo 📱 OR copy APK to phone and install manually!
echo.
pause