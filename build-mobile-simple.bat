@echo off
echo 📱 Building Mobile App (Simplified - No Assets)...
echo.

cd mobile_app

echo Step 1: Fixing dependencies...
npx expo install --fix

echo Step 2: Building Android APK (simplified)...
eas build --platform android --profile preview --clear-cache

echo.
echo ✅ Mobile app build initiated!
echo.
echo 📝 What's different:
echo   • Removed asset file requirements (icon, splash, etc.)
echo   • Using default Expo assets
echo   • Simplified configuration
echo.
echo 🔗 Monitor progress at:
echo https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler
echo.
pause