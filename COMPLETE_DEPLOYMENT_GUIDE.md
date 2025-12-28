# 🚀 Complete Deployment Guide - A → D → B → C

## Prerequisites
- Node.js 18+ installed
- Git repository on GitHub
- Railway account (free tier available)
- Vercel account (free tier available)
- Expo CLI installed: `npm install -g @expo/cli`

---

## Step A: Backend Deployment (Railway) ⚡

### 1. Quick Railway Deployment

**Option 1: Web Interface (Recommended)**
1. Go to [railway.app](https://railway.app)
2. Click "Start a New Project"
3. Select "Deploy from GitHub repo"
4. Choose your repository
5. Select the `backend` folder as root directory
6. Railway will auto-detect Python and deploy!

**Option 2: CLI Method**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
cd backend
railway init
railway up
```

### 2. Configure Environment Variables

In Railway dashboard → Variables, add:
```bash
SECRET_KEY=your-super-secret-jwt-key-make-it-very-long-and-random-123456789
DATABASE_URL=sqlite:///./visionary.db
DEBUG=False
ENVIRONMENT=production
```

### 3. Get Your Backend URL
After deployment, Railway gives you a URL like:
`https://backend-production-xxxx.up.railway.app`

**Save this URL - you'll need it for steps D and B!**

---

## Step D: AI Services Configuration 🤖

### 1. OpenAI Setup (Required for AI features)

**Get API Key:**
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up/login → API Keys → Create new key
3. Copy the key (starts with `sk-`)

**Add to Railway:**
```bash
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

**Add Credits:**
- Go to Billing → Add $10-20 to start
- DALL-E 3 costs ~$0.04 per image

### 2. Google Cloud Speech (Optional but recommended)

**Setup:**
1. [Google Cloud Console](https://console.cloud.google.com)
2. Create project → Enable "Speech-to-Text API"
3. Credentials → Create API Key
4. Copy the API key

**Add to Railway:**
```bash
GOOGLE_CLOUD_API_KEY=your-google-cloud-api-key-here
```

### 3. Test Your Backend
```bash
# Health check
curl https://your-backend-url.railway.app/health

# Should return: {"status": "healthy"}
```

---

## Step B: Web App Deployment (Vercel) 🌐

### 1. Update API Configuration

Edit `web_app/.env.production`:
```bash
REACT_APP_API_URL=https://your-backend-url.railway.app
REACT_APP_API_BASE_URL=https://your-backend-url.railway.app/api/v1
REACT_APP_ENVIRONMENT=production
```

### 2. Deploy to Vercel

**Option 1: Web Interface (Easiest)**
1. Go to [vercel.com](https://vercel.com)
2. Import your GitHub repository
3. Set Root Directory to `web_app`
4. Add Environment Variables:
   - `REACT_APP_API_URL`: Your Railway backend URL
   - `REACT_APP_API_BASE_URL`: Your Railway backend URL + `/api/v1`
5. Deploy!

**Option 2: CLI Method**
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd web_app
vercel --prod
```

### 3. Update CORS in Backend

Your web app URL will be something like: `https://visionary-web.vercel.app`

Update `backend/main.py` CORS settings:
```python
allow_origins=[
    "http://localhost:3000",
    "https://*.vercel.app",
    "https://your-actual-vercel-url.vercel.app"  # Add your actual URL
],
```

Redeploy backend after CORS update.

---

## Step C: Mobile App Preparation 📱

### 1. Update API Configuration

Create `mobile_app/.env`:
```bash
EXPO_PUBLIC_API_URL=https://your-backend-url.railway.app
EXPO_PUBLIC_API_BASE_URL=https://your-backend-url.railway.app/api/v1
```

### 2. Build for Testing

**Android APK (for testing):**
```bash
cd mobile_app
npx expo install --fix
eas build --platform android --profile preview
```

**iOS Build (requires Apple Developer account):**
```bash
eas build --platform ios --profile preview
```

### 3. App Store Preparation

**For Google Play Store:**
```bash
# Production Android build
eas build --platform android --profile production
```

**For Apple App Store:**
```bash
# Production iOS build  
eas build --platform ios --profile production
```

---

## 🎯 Quick Start Commands

Run these commands in order:

```bash
# 1. Deploy Backend
cd backend
# Go to railway.app and deploy via web interface

# 2. Configure AI Services
# Add OPENAI_API_KEY to Railway dashboard

# 3. Deploy Web App
cd ../web_app
# Update .env.production with your Railway URL
# Go to vercel.com and deploy via web interface

# 4. Build Mobile App
cd ../mobile_app
# Update .env with your Railway URL
npx expo install --fix
eas build --platform android --profile preview
```

---

## ✅ Deployment Checklist

### Backend (Railway):
- [ ] Backend deployed successfully
- [ ] Health endpoint returns `{"status": "healthy"}`
- [ ] Environment variables configured
- [ ] OpenAI API key added and working
- [ ] Google Cloud API key added (optional)

### Web App (Vercel):
- [ ] Web app deployed successfully
- [ ] API calls work (check browser network tab)
- [ ] Login/authentication works
- [ ] All pages load correctly
- [ ] PWA features work offline

### Mobile App (Expo):
- [ ] APK builds successfully
- [ ] App installs on test device
- [ ] API calls work from mobile
- [ ] Camera/microphone permissions work
- [ ] Push notifications configured

---

## 🚨 Troubleshooting

### Common Issues:

**Backend Issues:**
- `500 Internal Server Error`: Check Railway logs
- `CORS Error`: Update CORS origins in main.py
- `Database Error`: Check DATABASE_URL environment variable

**Web App Issues:**
- `Network Error`: Check API URL in .env.production
- `Build Failed`: Run `npm install` and check for TypeScript errors
- `404 on Refresh`: Vercel routing issue - check vercel.json

**Mobile App Issues:**
- `Build Failed`: Run `npx expo install --fix`
- `API Not Working`: Check .env file and network permissions
- `Camera Not Working`: Check app.json permissions

### Debug Commands:
```bash
# Check Railway logs
railway logs

# Check Vercel logs
vercel logs

# Test API locally
curl -X GET https://your-backend-url.railway.app/health
```

---

## 🎉 Success! What's Next?

Once deployed, you'll have:
- ✅ Live backend API with AI services
- ✅ Progressive web app accessible worldwide
- ✅ Mobile app ready for app stores
- ✅ Full cross-platform sync

**Next Steps:**
1. Test all features with real users
2. Set up monitoring and analytics
3. Prepare app store listings
4. Launch beta testing program
5. Scale based on user feedback

Your Visionary AI Personal Scheduler is now live! 🚀