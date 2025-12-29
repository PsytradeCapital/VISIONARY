@echo off
echo 📱 Building Visionary Mobile App (Fixed)...
echo.

cd mobile_app

echo Step 1: Building Android APK for testing...
echo This will take 5-10 minutes...
eas build --platform android --profile preview

echo.
echo ✅ Build process initiated!
echo.
echo 📝 What happens next:
echo 1. EAS will build your app in the cloud (5-10 minutes)
echo 2. You'll get a download link for the APK
echo 3. Install the APK on your Android device
echo 4. Test the app with your Railway backend
echo.
echo 🔗 Monitor build progress at:
echo https://expo.dev/accounts/martinmbugua300/projects/visionary-mobile/builds
echo.
pause