# 🚀 Railway Web Deployment - Complete Guide

## Quick Status Check
✅ Railway configuration files ready  
✅ Health check endpoint available  
✅ CORS properly configured  
✅ Requirements.txt complete  

## 1. Open Railway Dashboard
- Go to [railway.app](https://railway.app)
- Click "Login" → Sign in with GitHub

## 2. Deploy Your Backend
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your `VISIONARY` repository
- **IMPORTANT**: Click "Configure" and set:
  - Root Directory: `backend`
  - Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
  - Start Command: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

## 3. Railway Will Auto-Deploy
- Railway detects Python/FastAPI automatically
- Deployment takes 2-3 minutes
- You'll get a URL like: `https://backend-production-1a2b.up.railway.app`

## 4. Add Environment Variables
In Railway dashboard → Variables tab, click "Add Variable" for each:

```
SECRET_KEY = your-super-secret-jwt-key-make-it-very-long-and-random-123456789
DATABASE_URL = sqlite:///./visionary.db
DEBUG = False
ENVIRONMENT = production
OPENAI_API_KEY = sk-your-openai-key-here
```

## 5. Test Your Backend
Visit your Railway URL + `/health`:
`https://your-backend-url.railway.app/health`

Should return: `{"status": "healthy"}`

## 6. Copy Your Backend URL
Save this URL - you'll need it for the web app deployment!

---

## Next: Deploy Web App to Vercel

Once your backend is live, we'll deploy the web app to Vercel using the same web interface approach.

## 🔧 Troubleshooting Common Issues

### If Deployment Fails:
1. **Python Version**: Railway uses Python 3.11 by default
2. **Build Timeout**: Increase timeout in Railway settings
3. **Memory Issues**: Check if your app needs more RAM

### If Health Check Fails:
- Verify `/health` endpoint returns `{"status": "healthy"}`
- Check Railway logs for startup errors
- Ensure PORT environment variable is used

### Environment Variables Checklist:
```
SECRET_KEY = your-super-secret-jwt-key-make-it-very-long-and-random-123456789
DATABASE_URL = sqlite:///./visionary.db
DEBUG = False
ENVIRONMENT = production
OPENAI_API_KEY = sk-your-openai-key-here
PORT = (Railway sets this automatically)
```

## 🚀 Quick Redeploy
Run `redeploy-railway.bat` for a checklist, then:
1. Push changes to GitHub
2. Railway auto-deploys from main branch
3. Check deployment logs in Railway dashboard

## 🌐 Testing Your Deployment
1. Health check: `https://your-app.railway.app/health`
2. API docs: `https://your-app.railway.app/docs`
3. Root endpoint: `https://your-app.railway.app/`

---

## Next Steps After Backend is Live:
1. Copy your Railway backend URL
2. Update web app environment variables
3. Deploy web app to Vercel
4. Test full integration