# 📋 Quick Copy-Paste for Railway Variables

## Environment Variables to Add in Railway

Copy each line below and paste into Railway Variables tab:

### Variable 1: SECRET_KEY
```
Martin900mbugu#VisionaryAI2024$SuperSecretJWTKey!Railway@Deployment*FastAPI&Secure
```

### Variable 2: OPENAI_API_KEY
```
sk-...0DMA
```
*(Replace with your full OpenAI key)*

### Variable 3: DATABASE_URL
```
sqlite:///./visionary.db
```

### Variable 4: DEBUG
```
False
```

### Variable 5: ENVIRONMENT
```
production
```

### Variable 6: ALGORITHM
```
HS256
```

### Variable 7: ACCESS_TOKEN_EXPIRE_MINUTES
```
30
```

---

## 🎯 Railway Steps Summary

1. **Go to**: railway.app
2. **Login**: with GitHub
3. **New Project**: Deploy from GitHub repo
4. **Select**: VISIONARY repository
5. **Settings**: Change root directory to `backend`
6. **Variables**: Add all 7 variables above
7. **Test**: Visit your-url.railway.app/health

---

## ⚠️ Important Notes

- **Don't add quotes** around the values
- **No extra spaces** before or after values
- **Root directory MUST be** `backend` (not `/` or empty)
- **Wait 2-3 minutes** after adding variables for redeployment

---

## 🆘 If You Get Stuck

1. **Check Logs tab** in Railway for error messages
2. **Verify root directory** is set to `backend`
3. **Double-check** all variable names and values
4. **Try redeploying** by clicking "Redeploy" button