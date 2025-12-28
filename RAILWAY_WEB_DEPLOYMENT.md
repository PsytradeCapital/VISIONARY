# 🚀 Railway Web Deployment - Step by Step

Since the CLI had issues, let's use Railway's web interface (much easier!):

## 1. Open Railway Dashboard
- Go to [railway.app](https://railway.app)
- Click "Login" → Sign in with GitHub

## 2. Deploy Your Backend
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your `VISIONARY` repository
- **IMPORTANT**: Click "Configure" and set:
  - Root Directory: `backend`
  - Build Command: (leave empty - Railway auto-detects)
  - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

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