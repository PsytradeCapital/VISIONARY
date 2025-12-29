@echo off
echo 🔗 Testing Backend Integration...
echo.

echo Testing Railway Backend Health...
curl -s https://visionary-backend-production.up.railway.app/health
echo.
echo.

echo Testing API Endpoints...
echo 1. Health Check:
curl -s https://visionary-backend-production.up.railway.app/health | findstr "status"
echo.

echo 2. API Documentation:
curl -s -I https://visionary-backend-production.up.railway.app/docs | findstr "200"
echo.

echo 3. API Base Endpoint:
curl -s -I https://visionary-backend-production.up.railway.app/api/v1/ | findstr "200"
echo.

echo ✅ Backend Integration Test Complete!
echo.
echo 📝 Backend Status:
echo   • URL: https://visionary-backend-production.up.railway.app
echo   • API: https://visionary-backend-production.up.railway.app/api/v1
echo   • Docs: https://visionary-backend-production.up.railway.app/docs
echo.
pause