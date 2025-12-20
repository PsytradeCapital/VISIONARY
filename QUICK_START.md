# ⚡ Visionary - Quick Start Guide

## 🎯 **Fastest Way to View the Images**

### **Option 1: Simple HTML Viewer (No Installation Required!)**

1. **Double-click** `image-viewer.html`
2. Your browser will open showing all the design concepts
3. Click any image to see details

**That's it!** No installation, no setup, just instant access to the image gallery.

---

## 🚀 **Full Application Setup**

### **Prerequisites Check:**
```bash
python --version   # Should be 3.8 or higher
node --version     # Should be 16 or higher
npm --version      # Should be 7 or higher
```

Don't have them? Install:
- **Python**: https://www.python.org/downloads/
- **Node.js**: https://nodejs.org/downloads/

---

### **Step 1: Start Backend** (Terminal 1)

**Windows:**
```bash
# Double-click start-backend.bat
# OR manually:
cd backend
pip install -r requirements.txt
python main.py
```

**Mac/Linux:**
```bash
cd backend
pip3 install -r requirements.txt
python3 main.py
```

✅ Backend running at: http://localhost:8000

---

### **Step 2: Start Frontend** (Terminal 2 - New Window)

**Windows:**
```bash
# Double-click start-frontend.bat
# OR manually:
cd frontend
npm install
npm start
```

**Mac/Linux:**
```bash
cd frontend
npm install
npm start
```

✅ Frontend running at: http://localhost:3000

---

### **Step 3: Explore!**

Open your browser to: **http://localhost:3000**

**Login:** Use any email and password (demo mode)

**Navigate to:**
- 🏠 **Dashboard** - Main overview with featured images
- 📤 **Upload** - File upload interface
- 📅 **Schedule** - Calendar and scheduling views
- 📊 **Progress** - Goal tracking and analytics
- 🎨 **Gallery** - Browse all 19 design concepts ⭐
- 🔧 **Selector** - Interactive image analysis tool ⭐

---

## 🎨 **Image Gallery Features**

### **What You'll Find:**

1. **19 Professional Design Concepts**
   - Dashboard interfaces
   - Scheduling views
   - Analytics dashboards
   - Mobile designs
   - AI assistant interfaces

2. **AI-Powered Analysis**
   - Quality ratings (1-5 stars)
   - Category classifications
   - Use case recommendations
   - Color harmony analysis
   - Mobile optimization scores

3. **Interactive Tools**
   - Image selector with filters
   - Auto-selection by purpose
   - Comparison features
   - Detailed image information

---

## 🏆 **Best Images (Top 5)**

1. **image2.jpeg** ⭐⭐⭐⭐⭐ (4.8/5.0)
   - **Category**: Scheduling
   - **Best For**: Calendar views, schedule planning
   - **Why**: Highest rated, excellent usability

2. **image4.jpeg** ⭐⭐⭐⭐⭐ (4.7/5.0)
   - **Category**: AI Assistant
   - **Best For**: Chat interfaces, AI interactions
   - **Why**: Perfect for conversational features

3. **image3.jpeg** ⭐⭐⭐⭐☆ (4.6/5.0)
   - **Category**: Analytics
   - **Best For**: Progress tracking, data visualization
   - **Why**: Great for showing achievements

4. **image10.jpeg** ⭐⭐⭐⭐☆ (4.6/5.0)
   - **Category**: Goals
   - **Best For**: Goal setting, motivation
   - **Why**: Inspiring design for user engagement

5. **image1.jfif.jpeg** ⭐⭐⭐⭐☆ (4.5/5.0)
   - **Category**: Dashboard
   - **Best For**: Main interface, overview screens
   - **Why**: Professional and modern

---

## 🔧 **Troubleshooting**

### **Backend Won't Start:**
```bash
# Try installing dependencies individually:
pip install fastapi uvicorn sqlalchemy
pip install PyPDF2 python-docx
python main.py
```

### **Frontend Won't Start:**
```bash
# Clear cache and reinstall:
cd frontend
rm -rf node_modules package-lock.json
npm install
npm start
```

### **Port Already in Use:**
```bash
# Frontend on different port:
npm start -- --port 3001

# Backend on different port:
cd backend
uvicorn main:app --port 8001
```

### **Just Want to See Images:**
- Open `image-viewer.html` in your browser
- OR check `IMAGE_RECOMMENDATIONS.md` for detailed analysis
- OR browse `.kiro/specs/ai-personal-scheduler/` folder directly

---

## 📚 **Additional Resources**

- **IMAGE_RECOMMENDATIONS.md** - Detailed image analysis and recommendations
- **SETUP_GUIDE.md** - Comprehensive setup instructions
- **README.md** - Full project documentation
- **API Docs** - http://localhost:8000/docs (when backend is running)

---

## 💡 **Quick Tips**

1. **Frontend works independently** - You can explore the UI without the backend
2. **Demo mode enabled** - Login with any credentials to test the interface
3. **Images are pre-loaded** - All 19 designs are ready to view
4. **Mobile responsive** - Try resizing your browser window
5. **Best viewed in Chrome/Firefox** - For optimal experience

---

## 🎯 **What to Do First**

1. ✅ Open `image-viewer.html` to see all images instantly
2. ✅ Read `IMAGE_RECOMMENDATIONS.md` for detailed analysis
3. ✅ Start the frontend to explore interactive features
4. ✅ Navigate to `/gallery` to see the full gallery
5. ✅ Try the `/selector` tool for AI-powered recommendations

---

## 🆘 **Still Having Issues?**

**Option 1:** Just use the HTML viewer (`image-viewer.html`)
**Option 2:** Browse images directly in `.kiro/specs/ai-personal-scheduler/`
**Option 3:** Check `SETUP_GUIDE.md` for detailed troubleshooting

**Remember:** The image gallery and design analysis work even if you can't run the full application!

---

**Ready to explore? Start with `image-viewer.html` for instant access! 🚀**