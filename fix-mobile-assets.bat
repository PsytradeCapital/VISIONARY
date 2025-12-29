@echo off
echo 🔧 Fixing Mobile App Assets...
echo.

cd mobile_app

echo Step 1: Creating assets directory...
mkdir assets 2>nul

echo Step 2: Downloading default Expo assets...
curl -o assets/icon.png https://via.placeholder.com/1024x1024/ff6b35/ffffff?text=V
curl -o assets/adaptive-icon.png https://via.placeholder.com/1024x1024/ff6b35/ffffff?text=V
curl -o assets/splash.png https://via.placeholder.com/1284x2778/667eea/ffffff?text=Visionary
curl -o assets/favicon.png https://via.placeholder.com/48x48/ff6b35/ffffff?text=V

echo Step 3: Fixing package.json dependencies...
npm remove @types/react-native
npm install react-native@0.72.10

echo Step 4: Updating Expo SDK...
npx expo install --fix

echo.
echo ✅ Mobile app assets fixed!
echo.
pause