@echo off
echo Starting Visionary Frontend...
echo.

cd frontend

echo Installing Node.js dependencies...
npm install

echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:3000
echo.

npm start

pause