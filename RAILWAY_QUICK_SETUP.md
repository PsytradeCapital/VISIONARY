# 🚀 Railway Quick Setup - Final Steps

## ✅ Current Status:
- ✅ Railway project created: `visionary-backend`
- ✅ Service created and uploaded
- ❌ Environment variables needed
- ❌ Deployment failed (expected without env vars)

## 🔧 Complete Setup via Web Dashboard:

### 1. Open Your Project
Go to: https://railway.com/project/12cc0871-0a98-433f-a9dc-5752ace17ad4

### 2. Click on "visionary-backend" Service

### 3. Go to "Variables" Tab
Add these environment variables:

```
SECRET_KEY = your-super-secret-jwt-key-make-it-very-long-and-random-123456789
DATABASE_URL = sqlite:///./visionary.db
DEBUG = False
ENVIRONMENT = production
OPENAI_API_KEY = sk-your-openai-key-here
```

### 4. Go to "Settings" Tab
Verify these settings:
- **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`

### 5. Redeploy
- Click "Deploy" button or
- Go to "Deployments" tab and click "Redeploy"

### 6. Get Your URL
Once deployed, you'll get a URL like:
`https://visionary-backend-production-xxxx.up.railway.app`

---

## 🧪 Test Your Deployment

Visit these URLs to verify:
- Health check: `https://your-url.railway.app/health`
- API docs: `https://your-url.railway.app/docs`

Expected response from `/health`:
```json
{"status": "healthy"}
```

---

## 🎯 Next Steps After Backend is Live:

1. **Copy your Railway URL**
2. **Update web app config**:
   ```bash
   update-webapp-config.bat
   ```
3. **Deploy web app to Vercel**

---

**The web dashboard is faster and more reliable than CLI for environment variables!**