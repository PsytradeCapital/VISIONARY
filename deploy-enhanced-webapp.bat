@echo off
echo 🌐 Deploying Enhanced Web App to Vercel...
echo.

cd web_app

echo Step 1: Building enhanced web app...
npm run build

echo Step 2: Deploying to Vercel...
npx vercel --prod

echo.
echo ✅ Enhanced web app deployed!
echo.
echo 🎨 Visual Enhancements Applied:
echo   • Professional SVG icons (no more emojis)
echo   • Glassmorphism effects with backdrop blur
echo   • AI-themed gradients and animations
echo   • Neural network background patterns
echo   • Holographic text effects
echo   • Professional loading animations
echo   • Enhanced micro-interactions
echo.
echo 🔗 Your enhanced app: https://visionary-ai-web-app.vercel.app
echo.
pause