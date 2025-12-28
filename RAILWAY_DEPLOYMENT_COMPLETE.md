# 🚀 Complete Railway Deployment Guide

## Current Status: ✅ Logged in to Railway CLI

You're logged in as: `psytradecapital@gmail.com`

## Option 1: Web Interface (Recommended - Faster)

### 1. Go to Railway Dashboard
- Open: https://railway.app/dashboard
- You should see your workspace: "psytradecapital's Projects"

### 2. Create New Project
- Click "New Project"
- Select "Deploy from GitHub repo"
- Choose your repository (should show up if connected to GitHub)
- **IMPORTANT**: Set these settings:
  - **Root Directory**: `backend`
  - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
  - **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3. Add Environment Variables
Click "Variables" tab and add:
```
SECRET_KEY=your-super-secret-jwt-key-make-it-very-long-and-random-123456789
DATABASE_URL=sqlite:///./visionary.db
DEBUG=False
ENVIRONMENT=production
OPENAI_API_KEY=sk-your-openai-key-here
```

### 4. Deploy
- Click "Deploy"
- Wait 2-3 minutes for build
- Get your URL (something like: `https://backend-production-1a2b.up.railway.app`)

---

## Option 2: CLI Method (Alternative)

If you prefer CLI, here's the step-by-step:

### 1. Create Project Manually
```bash
# In a new terminal (the current one seems stuck)
cd backend
railway init
# When prompted:
# - Project Name: visionary-backend
# - Select: Empty Project
```

### 2. Set Environment Variables
```bash
railway variables set SECRET_KEY=your-super-secret-jwt-key-make-it-very-long-and-random-123456789
railway variables set DATABASE_URL=sqlite:///./visionary.db
railway variables set DEBUG=False
railway variables set ENVIRONMENT=production
railway variables set OPENAI_API_KEY=sk-your-openai-key-here
```

### 3. Deploy
```bash
railway up
```

---

## 🔧 Troubleshooting

### If CLI is Stuck:
1. Press `Ctrl+C` to cancel current command
2. Open a new terminal
3. Try the web interface method instead

### If Build Fails:
- Check Railway logs in dashboard
- Verify all files are in `backend/` directory
- Ensure `requirements.txt` is complete

### If Health Check Fails:
- Test locally first: `python -m uvicorn main:app --host 0.0.0.0 --port 8000`
- Visit: `http://localhost:8000/health`

---

## ✅ After Successful Deployment

1. **Test Your Backend**:
   - Visit: `https://your-app.railway.app/health`
   - Should return: `{"status": "healthy"}`

2. **Update Web App**:
   ```bash
   # Run this with your Railway URL
   update-webapp-config.bat
   ```

3. **Deploy Web App to Vercel**:
   - Go to vercel.com
   - Import your GitHub repo
   - Set root directory to `web_app`
   - Deploy!

---

## 🎯 Quick Commands Reference

```bash
# Check Railway status
railway status

# View logs
railway logs

# Open in browser
railway open

# List projects
railway list
```

**Recommendation**: Use the web interface method - it's more reliable and visual!