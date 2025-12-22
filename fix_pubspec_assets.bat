@echo off
echo Fixing pubspec.yaml asset issues...

REM Copy clean pubspec.yaml
echo Copying clean pubspec.yaml...
copy "pubspec_clean.yaml" "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\pubspec.yaml" /Y

REM Create missing asset directories (optional for future use)
echo Creating asset directories for future use...
mkdir "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\assets\images" 2>nul
mkdir "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\assets\icons" 2>nul
mkdir "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\assets\fonts" 2>nul

echo pubspec.yaml fixed and directories created!

echo.
echo Getting dependencies...
cd "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh"
flutter pub get

echo.
echo Now building the app...
flutter build apk --debug

echo.
echo Build completed!
pause