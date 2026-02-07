# DEPLOY TO RENDER NOW

## Your Gemini API Key (SAVED):
```
AIzaSyBt9Hsvp5WvQojknKKgacJf4r9zPM5dC1M
```

## Step-by-Step Deployment:

### 1. Go to Render Dashboard
https://dashboard.render.com/register

### 2. Sign Up (Free)
- Use your email or GitHub

### 3. Create New Web Service
- Click "New +" button
- Select "Web Service"

### 4. Connect Repository
**Option A: GitHub (Recommended)**
- Click "Connect GitHub"
- Select your repository
- Click "Connect"

**Option B: Public Git URL**
- Paste your repo URL
- Click "Continue"

### 5. Configure Service
Fill in these EXACT values:

**Name:** `visionary-backend`

**Environment:** `Python 3`

**Region:** `Oregon (US West)` (or closest to you)

**Branch:** `main` (or your default branch)

**Build Command:**
```
cd backend && pip install -r requirements.txt
```

**Start Command:**
```
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Plan:** `Free`

### 6. Add Environment Variables
Click "Advanced" → "Add Environment Variable"

Add these THREE variables:

**Variable 1:**
- Key: `GEMINI_API_KEY`
- Value: `AIzaSyBt9Hsvp5WvQojknKKgacJf4r9zPM5dC1M`

**Variable 2:**
- Key: `SECRET_KEY`
- Value: `visionary-super-secret-key-change-in-production-32chars-min`

**Variable 3:**
- Key: `DATABASE_URL`
- Value: `sqlite+aiosqlite:///./visionary.db`

### 7. Create Web Service
- Click "Create Web Service"
- Wait 5-10 minutes for deployment

### 8. Get Your Backend URL
After deployment completes, you'll see:
```
https://visionary-backend.onrender.com
```

Copy this URL!

### 9. Update Mobile App
Edit `mobile_app/.env`:
```
EXPO_PUBLIC_API_URL=https://visionary-backend.onrender.com/api/v1
```

### 10. Test Backend
Open in browser:
```
https://visionary-backend.onrender.com/health
```

Should return: `{"status":"healthy"}`

### 11. Build Mobile App
```bash
cd mobile_app
npm install
eas build --platform android --profile preview
```

## DONE!

Your app is now:
✅ Using real Gemini AI
✅ Deployed on Render (FREE)
✅ No demo mode
✅ Real backend integration
✅ Actually working

## Troubleshooting

**If deployment fails:**
1. Check Render logs (click "Logs" tab)
2. Verify environment variables are set
3. Make sure build/start commands are correct

**If health check fails:**
1. Wait 2-3 minutes after deployment
2. Render free tier may take time to start
3. Check logs for errors

**Need help?**
- Render docs: https://render.com/docs
- Check deployment logs in Render dashboard
