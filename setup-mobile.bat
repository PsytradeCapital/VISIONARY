@echo off
echo 📱 Setting up Visionary AI for Mobile Installation
echo.

echo 🎨 Generating app icons...
node generate-icons.js

echo.
echo 🚀 Starting development server...
cd frontend
npm start

echo.
echo ✅ Setup complete!
echo.
echo 📱 To install on mobile:
echo 1. Find your IP address: ipconfig
echo 2. On mobile, visit: http://YOUR_IP:3000
echo 3. iPhone: Safari > Share > Add to Home Screen
echo 4. Android: Chrome > Menu > Add to Home Screen
echo.
echo 🎨 To generate PNG icons:
echo Visit: http://localhost:3000/generate-icons.html
echo.
pause