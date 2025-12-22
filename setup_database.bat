@echo off
echo Setting up Visionary AI Database...
echo.

REM Stop any running backend server first
echo Stopping any running backend servers...
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Initializing database tables...
python init_database.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Database setup completed successfully!
    echo.
    echo Now starting the backend server...
    echo.
    
    REM Change to backend directory and start server
    cd /d "C:\Users\Martin Mbugua\Desktop\VISIONARY\backend"
    echo Starting backend server on http://0.0.0.0:8000...
    python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
) else (
    echo.
    echo ❌ Database setup failed!
    echo Please check the error messages above.
    pause
)

echo.
pause