# 🚀 Simple Deployment Guide - Web Interface Method

Since the CLI approach had issues, let's use the web interfaces which are more reliable and user-friendly.

## Step A: Deploy Backend to Railway (5 minutes)

### 1. Go to Railway
- Open [railway.app](https://railway.app) in your browser
- Click "Login" and sign in with GitHub

### 2. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your `VISIONARY` repository
- **Important**: Set root directory to `backend`

### 3. Railway Auto-Deploys
- Railway detects Python and automatically deploys
- Wait 2-3 minutes for deployment to complete
- You'll get a URL like: `https://backend-production-xxxx.up.railway.app`

### 4. Add Environment Variables
In Railway dashboard → Variables tab, add:
```
SECRET_KEY=your-super-secret-jwt-key-make-it-very-long-and-random-123456789
DATABASE_URL=sqlite:///./visionary.db
DEBUG=False
ENVIRONMENT=production
```

### 5. Test Backend
Visit: `https://your-backend-url.railway.app/health`
Should return: `{"status": "healthy"}`

---

## Step D: Configure AI Services (2 minutes)

### 1. Get OpenAI API Key
- Go to [platform.openai.com](https://platform.openai.com)
- Sign up/login → API Keys → Create new key
- Copy the key (starts with `sk-`)

### 2. Add to Railway
In Railway dashboard → Variables, add:
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

### 3. Add Credits
- In OpenAI dashboard → Billing
- Add $10-20 to start testing

---

## Step B: Deploy Web App to Vercel (3 minutes)

### 1. Update Web App Config
First, update your backend URL in the web app.