@echo off
echo 📱 Building Visionary Mobile App...
echo.

set /p BACKEND_URL="Enter your Railway backend URL (e.g., https://backend-production-xxxx.up.railway.app): "

if "%BACKEND_URL%"=="" (
    echo ❌ Error: Backend URL is required
    pause
    exit /b 1
)

echo Step 1: Updating mobile app configuration...
cd mobile_app

echo EXPO_PUBLIC_API_URL=%BACKEND_URL% > .env
echo EXPO_PUBLIC_API_BASE_URL=%BACKEND_URL%/api/v1 >> .env

echo ✅ Environment configured
echo.

echo Step 2: Installing dependencies...
npm install
npx expo install --fix
echo.

echo Step 3: Installing EAS CLI...
npm install -g @expo/cli eas-cli
echo.

echo Step 4: Logging into Expo...
echo Please login to Expo in the browser window that opens...
npx expo login
echo.

echo Step 5: Building Android APK for testing...
echo This will take 5-10 minutes...
eas build --platform android --profile preview
echo.

echo ✅ Mobile app build complete!
echo.
echo 📝 Next steps:
echo 1. Download the APK from the Expo dashboard
echo 2. Install on your Android device for testing
echo 3. For iOS, run: eas build --platform ios --profile preview
echo 4. For production builds, use --profile production
echo.
pause