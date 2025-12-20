@echo off
echo 🔍 Searching for Flutter installation...
echo.

REM Method 1: Check registry for Flutter
echo Checking Windows Registry...
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s /f "Flutter" 2>nul | findstr "InstallLocation"

echo.
echo Checking common directories...

REM Method 2: Check common directories
for %%d in (
    "C:\flutter"
    "C:\src\flutter" 
    "%USERPROFILE%\flutter"
    "%USERPROFILE%\Downloads\flutter"
    "%USERPROFILE%\Desktop\flutter"
    "%USERPROFILE%\Documents\flutter"
    "C:\Program Files\flutter"
    "C:\Program Files (x86)\flutter"
    "%LOCALAPPDATA%\flutter"
    "%APPDATA%\flutter"
) do (
    if exist "%%~d\bin\flutter.exe" (
        echo ✅ FOUND: %%~d\bin\flutter.exe
        "%%~d\bin\flutter.exe" --version
        echo.
    )
)

echo.
echo 🔍 Searching entire C: drive (this may take a moment)...
dir C:\flutter.exe /s /b 2>nul

pause