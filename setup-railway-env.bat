@echo off
echo 🔧 Setting up Railway Environment Variables
echo ==========================================

echo.
echo Setting environment variables for visionary-backend service...
echo.

echo Setting SECRET_KEY...
railway variables --set "SECRET_KEY=your-super-secret-jwt-key-make-it-very-long-and-random-123456789" --service visionary-backend

echo Setting DATABASE_URL...
railway variables --set "DATABASE_URL=sqlite:///./visionary.db" --service visionary-backend

echo Setting DEBUG...
railway variables --set "DEBUG=False" --service visionary-backend

echo Setting ENVIRONMENT...
railway variables --set "ENVIRONMENT=production" --service visionary-backend

echo.
set /p OPENAI_KEY="Enter your OpenAI API key (sk-...): "
if not "%OPENAI_KEY%"=="" (
    echo Setting OPENAI_API_KEY...
    railway variables --set "OPENAI_API_KEY=%OPENAI_KEY%" --service visionary-backend
)

echo.
echo ✅ Environment variables set!
echo.
echo 🚀 Now deploying...
railway up --service visionary-backend

echo.
echo 🌐 Getting deployment status...
railway status --service visionary-backend

echo.
echo ✅ Deployment complete!
echo Check your Railway dashboard for the live URL.
pause