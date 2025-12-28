# 🚀 Visionary AI Deployment Guide

## Step A: Backend Deployment (Railway)

### 1. Sign up for Railway
- Go to [railway.app](https://railway.app)
- Sign up with GitHub account
- Connect your repository

### 2. Deploy Backend
```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Or deploy via web interface:
# 1. Click "New Project" 
# 2. Select "Deploy from GitHub repo"
# 3. Choose your repository
# 4. Select the backend folder
```

### 3. Configure Environment Variables
In Railway dashboard, add these variables:
```
SECRET_KEY=your-super-secret-jwt-key-here-make-it-long-and-random
DATABASE_URL=sqlite:///./visionary.db
DEBUG=False
ENVIRONMENT=production
```

### 4. Your Backend URL
After deployment, Railway will give you a URL like:
`https://your-app-name.railway.app`

---

## Step D: AI Services Configuration

### 1. OpenAI API Setup
- Go to [platform.openai.com](https://platform.openai.com)
- Create account and get API key
- Add to Railway environment variables:
```
OPENAI_API_KEY=sk-your-openai-key-here
```

### 2. Google Cloud Speech-to-Text
- Go to [Google Cloud Console](https://console.cloud.google.com)
- Enable Speech-to-Text API
- Create service account and download JSON key
- Add to Railway:
```
GOOGLE_CLOUD_API_KEY=your-google-cloud-key-here
```

---

## Step B: Web App Deployment (Vercel)

### 1. Prepare Web App
Update your web app's API base URL to point to Railway backend.

### 2. Deploy to Vercel
```bash
cd web_app
npm install -g vercel
vercel --prod
```

---

## Step C: Mobile App Preparation

### 1. Update API URLs
Point mobile app to your Railway backend URL.

### 2. Build for Production
```bash
cd mobile_app
expo build:android
expo build:ios
```

## 🎯 Next Steps After Deployment

1. Test all endpoints with your live backend
2. Configure custom domain (optional)
3. Set up monitoring and analytics
4. Prepare app store submissions
5. Launch beta testing

## 🔧 Troubleshooting

### Common Issues:
- **CORS errors**: Update CORS origins in main.py
- **Database issues**: Check DATABASE_URL environment variable
- **API key errors**: Verify all environment variables are set

### Health Check:
Your backend health endpoint: `https://your-app.railway.app/health`