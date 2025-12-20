@echo off
echo Fixing Frontend Dependencies...
echo.

cd frontend

echo Clearing npm cache and node_modules...
rmdir /s /q node_modules 2>nul
del package-lock.json 2>nul

echo.
echo Installing with legacy peer deps (fixes TypeScript conflict)...
npm install --legacy-peer-deps

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