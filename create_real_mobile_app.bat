@echo off
echo 🚀 Creating REAL Visionary AI Mobile App
echo.

echo 🧹 Cleaning up old Flutter attempts...
if exist "visionary_flutter" rmdir /s /q "visionary_flutter"
if exist "visionary_ai_mobile" rmdir /s /q "visionary_ai_mobile"
if exist "flutter_app" rmdir /s /q "flutter_app"

echo.
echo 📱 Creating new Flutter project...
flutter create visionary_mobile --org com.visionary.ai --project-name visionary_mobile

echo.
echo 📂 Project created at: visionary_mobile\
echo.

cd visionary_mobile

echo 📦 Adding required dependencies...
flutter pub add http
flutter pub add dio
flutter pub add provider
flutter pub add shared_preferences
flutter pub add file_picker
flutter pub add image_picker
flutter pub add permission_handler
flutter pub add record
flutter pub add audioplayers
flutter pub add flutter_secure_storage

echo.
echo ✅ Flutter project ready!
echo 📍 Location: visionary_mobile\
echo.
echo 🔥 Next: I'll create all the screens and connect to your backend!
pause