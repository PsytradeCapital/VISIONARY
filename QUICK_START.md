# QUICK START - REAL DEPLOYMENT

## ✅ WHAT'S READY:

1. **Gemini API Key**: AIzaSyBt9Hsvp5WvQojknKKgacJf4r9zPM5dC1M (saved in backend/.env)
2. **Backend Code**: Updated with Gemini AI integration
3. **Mobile App**: Configured to connect to real backend
4. **No Demo Mode**: Everything uses real API

## 🚀 DEPLOY NOW (3 STEPS):

### Step 1: Deploy Backend to Render (5 minutes)
1. Go to: https://dashboard.render.com/register
2. Sign up (free)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Use these settings:
   - **Build**: `cd backend && pip install -r requirements.txt`
   - **Start**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables**:
     - `GEMINI_API_KEY`: `AIzaSyBt9Hsvp5WvQojknKKgacJf4r9zPM5dC1M`
     - `SECRET_KEY`: `visionary-super-secret-key-change-in-production-32chars-min`
     - `DATABASE_URL`: `sqlite+aiosqlite:///./visionary.db`
6. Click "Create Web Service"
7. Wait 5-10 minutes

### Step 2: Test Backend
Open: `https://your-app-name.onrender.com/health`

Should see: `{"status":"healthy"}`

### Step 3: Build Mobile App
```bash
cd mobile_app
npm install
eas build --platform android --profile preview
```

## 📱 MOBILE APP:
- Already configured with: `https://visionary-backend.onrender.com/api/v1`
- Update this URL after your Render deployment

## 🧪 TEST LOCALLY FIRST (Optional):
```bash
test-backend-local.bat
```
Then visit: http://localhost:8000/docs

## 📖 DETAILED INSTRUCTIONS:
See `RENDER_DEPLOY_INSTRUCTIONS.md` for step-by-step with screenshots

## ✅ WHAT YOU GET:
- Real Gemini AI schedule generation
- Real document processing
- Real progress tracking
- Real motivational content
- NO DEMO MODE
- 100% FREE (Render + Gemini)

Your backend is ready to deploy RIGHT NOW!
