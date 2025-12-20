@echo off
echo ========================================
echo    Visionary - Frontend Only Mode
echo ========================================
echo.
echo This will start just the frontend with:
echo - Image Gallery (19 design concepts)
echo - Image Selector Tool
echo - Interactive Design Analysis
echo - Demo Mode (no backend required)
echo.

cd frontend

echo Installing Node.js dependencies...
npm install

echo.
echo Starting React development server...
echo.
echo ========================================
echo   🎨 VISIONARY IMAGE GALLERY
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Gallery:   http://localhost:3000/gallery
echo Selector:  http://localhost:3000/selector
echo.
echo Login with ANY email/password
echo.

npm start

pause