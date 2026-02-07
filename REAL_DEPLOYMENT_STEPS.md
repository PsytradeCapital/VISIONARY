# REAL DEPLOYMENT - NO TOYS

## 1. GET GEMINI API KEY (FREE)

1. Go to: https://makersuite.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key (starts with AIzaSy...)

## 2. DEPLOY BACKEND TO RENDER (FREE)

### Option A: Using Render Dashboard
1. Go to: https://dashboard.render.com
2. Sign up/Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repo OR use "Deploy from Git URL"
5. Settings:
   - **Name**: visionary-backend
   - **Environment**: Python 3
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free
6. Environment Variables:
   - `GEMINI_API_KEY`: (paste your key from step 1)
   - `SECRET_KEY`: (generate random 32+ characters)
   - `DATABASE_URL`: `sqlite+aiosqlite:///./visionary.db`
7. Click "Create Web Service"
8. Wait 5-10 minutes for deployment
9. Your backend URL: `https://visionary-backend.onrender.com`

### Option B: Using CLI
```bash
# Install Render CLI
npm install -g render-cli

# Deploy
render deploy
```

## 3. UPDATE MOBILE APP WITH BACKEND URL

Edit `mobile_app/.env`:
```
EXPO_PUBLIC_API_URL=https://visionary-backend.onrender.com/api/v1
```

## 4. UPDATE WEB APP WITH BACKEND URL

Edit `web_app/.env.production`:
```
REACT_APP_API_URL=https://visionary-backend.onrender.com/api/v1
```

## 5. TEST BACKEND

```bash
curl https://visionary-backend.onrender.com/health
```

Should return: `{"status":"healthy"}`

## 6. BUILD AND TEST MOBILE APP

```bash
cd mobile_app
npm install
eas build --platform android --profile preview
```

## DONE

No demo mode. No toys. Real backend with Gemini AI.
