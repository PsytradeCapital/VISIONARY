@echo off
echo 🚀 Starting Visionary AI Backend (Simple Mode)
echo.

echo 📦 Installing required packages...
cd backend
pip install fastapi uvicorn sqlalchemy aiosqlite python-multipart PyPDF2 python-docx

echo.
echo 🗄️ Using SQLite database for easy setup...
echo 🔧 Database will be created automatically at: ./visionary.db
echo.

echo 🚀 Starting backend server...
echo 📍 Backend will be available at: http://localhost:8000
echo 📖 API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause