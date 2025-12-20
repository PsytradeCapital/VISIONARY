# 🚀 Visionary Setup Guide (Without Docker)

Since Docker Compose is not available, here are alternative ways to run the Visionary AI Personal Scheduler:

## **Prerequisites**

### Required Software:
1. **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
2. **Node.js 16+** - [Download from nodejs.org](https://nodejs.org/downloads/)
3. **Git** (optional) - For version control

### Check if you have them:
```bash
python --version
node --version
npm --version
```

---

## **Method 1: Quick Start (Easiest)**

### Step 1: Start Backend
```bash
# Double-click start-backend.bat
# OR run manually:
cd backend
pip install -r requirements.txt
python main.py
```

### Step 2: Start Frontend (New Terminal)
```bash
# Double-click start-frontend.bat  
# OR run manually:
cd frontend
npm install
npm start
```

### Step 3: Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## **Method 2: Manual Step-by-Step**

### Backend Setup:
```bash
cd backend
pip install fastapi uvicorn sqlalchemy asyncpg redis python-jose passlib python-multipart pydantic pytest httpx hypothesis PyPDF2 python-docx
python main.py
```

### Frontend Setup (New Terminal):
```bash
cd frontend
npm install
npm start
```

---

## **Method 3: Simplified Demo Mode**

If you encounter issues with the full setup, you can run just the frontend to explore the image gallery and design features:

```bash
cd frontend
npm install
npm start
```

Then navigate to:
- http://localhost:3000/gallery - Image Gallery
- http://localhost:3000/selector - Image Selector Tool

---

## **Troubleshooting**

### Python Issues:
```bash
# If pip is not found:
python -m pip install -r requirements.txt

# If Python is not found, install from:
# https://www.python.org/downloads/
```

### Node.js Issues:
```bash
# If npm is not found, install Node.js from:
# https://nodejs.org/downloads/

# Clear npm cache if needed:
npm cache clean --force
```

### Port Conflicts:
If ports 3000 or 8000 are busy:
```bash
# Frontend on different port:
npm start -- --port 3001

# Backend on different port:
uvicorn main:app --port 8001
```

---

## **What You'll See**

### 🎨 **Image Gallery Features**
- **19 curated design concepts** with ratings
- **Interactive image viewer** with detailed analysis
- **AI-powered recommendations** for best image combinations
- **Color harmony analysis** and compatibility checking
- **Mobile optimization** indicators
- **Accessibility scores** for each design

### 📊 **Best Images to Explore**
1. **image2.jpeg** (4.8★) - Schedule Planning Interface
2. **image4.jpeg** (4.7★) - AI Assistant Chat Design  
3. **image3.jpeg** (4.6★) - Progress Tracking Dashboard
4. **image10.jpeg** (4.6★) - Goal Setting Interface
5. **image1.jfif.jpeg** (4.5★) - Main Dashboard Design

### 🧭 **Navigation**
- **Dashboard** - Main overview with featured images
- **Upload** - File upload interface (demo mode)
- **Schedule** - Calendar and scheduling views
- **Progress** - Goal tracking and analytics
- **Gallery** - Browse all 19 design concepts
- **Selector** - Interactive image analysis tool

---

## **Demo Mode**

The application includes demo data and mock authentication, so you can:
- ✅ Login with any email/password
- ✅ Explore all interface designs
- ✅ Use the image gallery and selector
- ✅ See progress tracking mockups
- ✅ View scheduling interfaces

---

## **Next Steps**

1. **Start with the frontend** to explore the image gallery
2. **Check out the Image Selector** for AI-powered recommendations
3. **Review IMAGE_RECOMMENDATIONS.md** for detailed analysis
4. **Use the best-rated images** for your own projects

---

## **Need Help?**

If you encounter any issues:
1. Check that Python and Node.js are properly installed
2. Make sure you're in the correct directory (backend/ or frontend/)
3. Try running commands one by one instead of using the batch files
4. Check the console for specific error messages

**The image gallery and design tools work independently of the backend, so you can explore those features even if the backend setup has issues!**

---

**Happy exploring! 🎨✨**