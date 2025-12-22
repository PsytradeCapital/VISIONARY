@echo off
echo Fixing all Flutter errors...

REM Copy clean files to visionary_mobile_fresh
echo Copying clean upload_screen.dart...
copy "upload_screen_clean.dart" "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\lib\screens\home\upload_screen.dart" /Y

echo Copying clean splash_screen.dart...
copy "splash_screen_clean.dart" "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\lib\screens\splash_screen.dart" /Y

echo Copying clean api_service.dart...
copy "api_service_clean.dart" "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\lib\services\api_service.dart" /Y

echo Copying clean widget_test.dart...
copy "widget_test_clean.dart" "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\test\widget_test.dart" /Y

echo Files copied successfully!
echo.
echo Now testing the fixes...
cd "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh"
flutter analyze

echo.
echo If no errors above, your Flutter app is now fixed!
echo You can now run: flutter build apk --debug
echo.
pause