@echo off
echo ========================================
echo    Visionary - Frontend Only Mode
echo ========================================
echo.
echo This will start just the frontend with:
echo - Live Interactive Dashboard
echo - AI Upload Portal
echo - Schedule & Progress Views
echo - Professional Animations
echo.

cd frontend

REM Check if node_modules exists
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
    echo.
) else (
    echo Dependencies already installed, skipping npm install...
    echo.
)

echo Starting React development server...
echo.
echo ========================================
echo   🚀 VISIONARY AI SCHEDULER
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Dashboard: http://localhost:3000/
echo Upload:    http://localhost:3000/upload
echo Schedule:  http://localhost:3000/schedule
echo Progress:  http://localhost:3000/progress
echo.
echo Login with ANY email/password
echo.

npm start

pause