@echo off
echo 📱 Continuing Mobile App Build Process...
echo.

echo Step 1: Navigate to mobile app directory...
cd mobile_app

echo Step 2: Login to Expo (this will open your browser)...
echo Please complete the login in your browser, then return here and press any key...
npx expo login
pause

echo Step 3: Building Android APK (this takes 5-10 minutes)...
echo Building for testing/preview...
eas build --platform android --profile preview

echo.
echo ✅ Build process initiated!
echo.
echo 📝 What happens next:
echo 1. EAS will build your app in the cloud
echo 2. You'll get a link to download the APK
echo 3. Install the APK on your Android device
echo 4. Test the app with your Railway backend
echo.
echo 🔗 Monitor build progress at: https://expo.dev/accounts/[your-username]/projects/visionary-mobile/builds
echo.
pause