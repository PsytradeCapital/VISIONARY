@echo off
echo Starting Visionary Frontend...
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
echo Frontend will be available at: http://localhost:3000
echo.

npm start

pause