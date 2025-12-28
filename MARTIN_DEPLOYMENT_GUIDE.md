# 🚀 Martin's Complete Railway Deployment Guide

## Your API Keys & Secrets

### ✅ OpenAI API Key (You Have This)
```
OPENAI_API_KEY = sk-...0DMA
```

### 🔑 SECRET_KEY (Generated for You)
```
SECRET_KEY = Martin900mbugu#VisionaryAI2024$SuperSecretJWTKey!Railway@Deployment*FastAPI&Secure
```

### 📋 All Environment Variables for Railway
Copy these EXACTLY into Railway:

```
SECRET_KEY = Martin900mbugu#VisionaryAI2024$SuperSecretJWTKey!Railway@Deployment*FastAPI&Secure
OPENAI_API_KEY = sk-...0DMA
DATABASE_URL = sqlite:///./visionary.db
DEBUG = False
ENVIRONMENT = production
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

---

## 🎯 Step-by-Step Railway Deployment

### Step 1: Open Railway
1. Go to **railway.app** in your browser
2. Click **"Login"**
3. Choose **"Continue with GitHub"**
4. Sign in with your GitHub account

### Step 2: Create New Project
1. Click the big **"New Project"** button
2. Select **"Deploy from GitHub repo"**
3. Find and click your **"VISIONARY"** repository
4. Click **"Deploy Now"**

### Step 3: Configure Root Directory
⚠️ **IMPORTANT**: Railway might deploy the wrong folder!

1. In Railway dashboard, click **"Settings"** tab
2. Find **"Root Directory"** setting
3. Change it from `/` to **`backend`**
4. Click **"Save"**
5. Railway will redeploy automatically

### Step 4: Add Environment Variables
1. Click **"Variables"** tab in Railway dashboard
2. Click **"Add Variable"** button
3. Add each variable one by one:

**Variable 1:**
- Name: `SECRET_KEY`
- Value: `Martin900mbugu#VisionaryAI2024$SuperSecretJWTKey!Railway@Deployment*FastAPI&Secure`

**Variable 2:**
- Name: `OPENAI_API_KEY`
- Value: `sk-...0DMA` (your full key)

**Variable 3:**
- Name: `DATABASE_URL`
- Value: `sqlite:///./visionary.db`

**Variable 4:**
- Name: `DEBUG`
- Value: `False`

**Variable 5:**
- Name: `ENVIRONMENT`
- Value: `production`

**Variable 6:**
- Name: `ALGORITHM`
- Value: `HS256`

**Variable 7:**
- Name: `ACCESS_TOKEN_EXPIRE_MINUTES`
- Value: `30`

### Step 5: Wait for Deployment
- Railway will automatically redeploy after adding variables
- Wait 2-3 minutes for deployment to complete
- Look for **"Success"** status

### Step 6: Get Your Backend URL
1. In Railway dashboard, click **"Deployments"** tab
2. Click on the latest deployment
3. Copy the **"Domain"** URL
4. It looks like: `https://backend-production-1a2b.up.railway.app`

### Step 7: Test Your Backend
1. Open a new browser tab
2. Go to: `https://your-backend-url.railway.app/health`
3. You should see: `{"status": "healthy"}`

---

## 🚨 Troubleshooting

### If Deployment Fails:
1. Check **"Logs"** tab in Railway
2. Look for error messages
3. Most common issue: Wrong root directory (should be `backend`)

### If Health Check Fails:
1. Check all environment variables are added correctly
2. Make sure `SECRET_KEY` has no extra spaces
3. Verify `OPENAI_API_KEY` is complete

### If Variables Won't Save:
1. Make sure there are no spaces before/after the values
2. Don't use quotes around the values
3. Click "Save" after each variable

---

## ✅ Success Checklist

- [ ] Railway account created with GitHub
- [ ] VISIONARY repository deployed
- [ ] Root directory set to `backend`
- [ ] All 7 environment variables added
- [ ] Deployment shows "Success" status
- [ ] Health check URL returns `{"status": "healthy"}`
- [ ] Backend URL copied and saved

---

## 🎉 What's Your Backend URL?

Once deployed, your backend will be available at:
`https://backend-production-XXXX.up.railway.app`

**Save this URL - you'll need it for the web app deployment!**

---

## Next Steps After Backend is Live:

1. **Test the backend** - Visit the health endpoint
2. **Deploy web app** - Use the web app deployment guide
3. **Build mobile app** - Use Expo to create APK
4. **Celebrate** - Your AI scheduler is going live! 🚀