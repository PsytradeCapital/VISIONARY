@echo off
echo Fixing network connection for real device...

REM Copy the updated API service with correct IP address
echo Copying updated API service with real device IP (192.168.100.93)...
copy "api_service_real_device.dart" "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\lib\services\api_service.dart" /Y

echo API service updated successfully!

echo.
echo Now rebuilding the app with the correct IP address...
cd /d "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh"

echo Hot reloading the app...
echo Press 'r' in your Flutter run terminal to hot reload
echo Or press 'R' to hot restart the app

echo.
echo The app should now connect to your backend at 192.168.100.93:8000
echo.
pause