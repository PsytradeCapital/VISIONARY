# 🤖 AI Services Configuration Guide

## Step D: Configure External AI Services

Your Visionary app uses these AI services:
- **OpenAI API** - For DALL-E 3 image generation and GPT processing
- **Google Cloud Speech-to-Text** - For voice input processing

### 1. OpenAI API Setup

#### Get Your API Key:
1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to API Keys section
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)

#### Add Credits:
- Go to Billing section
- Add payment method
- Add $10-20 credits to start
- DALL-E 3 costs ~$0.04 per image

### 2. Google Cloud Speech-to-Text Setup

#### Enable the API:
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project or select existing
3. Enable "Cloud Speech-to-Text API"
4. Go to "Credentials" section
5. Create "Service Account Key"
6. Download JSON key file

#### Get API Key:
1. In Google Cloud Console
2. Go to "APIs & Services" > "Credentials"
3. Click "Create Credentials" > "API Key"
4. Copy the API key

### 3. Add to Railway Environment Variables

In your Railway dashboard, add these environment variables:

```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# Google Cloud Configuration  
GOOGLE_CLOUD_API_KEY=your-google-cloud-api-key-here
GOOGLE_APPLICATION_CREDENTIALS=/app/google-credentials.json

# Optional: Additional AI Services
WEATHER_API_KEY=your-weather-api-key-here
```

### 4. Upload Google Credentials to Railway

For the Google service account JSON:
1. In Railway dashboard, go to Variables
2. Add new variable: `GOOGLE_CREDENTIALS_JSON`
3. Paste the entire JSON content as the value
4. Your app will create the credentials file automatically

### 5. Test Your AI Services

After deployment, test the endpoints:

```bash
# Test OpenAI integration
curl -X POST https://your-app.railway.app/api/ai/generate-image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful sunset over mountains"}'

# Test Google Speech
curl -X POST https://your-app.railway.app/api/ai/speech-to-text \
  -H "Content-Type: application/json" \
  -d '{"audio_data": "base64-encoded-audio"}'
```

## 💰 Cost Estimates

### OpenAI Pricing:
- **DALL-E 3**: $0.040 per image (1024×1024)
- **GPT-4**: $0.03 per 1K tokens input, $0.06 per 1K tokens output
- **GPT-3.5-turbo**: $0.001 per 1K tokens

### Google Cloud Pricing:
- **Speech-to-Text**: $0.006 per 15 seconds of audio
- **First 60 minutes per month**: FREE

### Monthly Estimates (100 active users):
- Image generation (50 images/month): $2.00
- Text processing (10K requests): $5.00
- Speech processing (500 minutes): $3.00
- **Total**: ~$10/month

## 🔒 Security Best Practices

1. **Never commit API keys** to your repository
2. **Use environment variables** for all secrets
3. **Rotate keys regularly** (every 90 days)
4. **Monitor usage** to detect anomalies
5. **Set spending limits** in OpenAI dashboard

## 🚨 Troubleshooting

### Common Issues:

**OpenAI API Errors:**
- `401 Unauthorized`: Check API key is correct
- `429 Rate Limited`: You've hit usage limits
- `402 Payment Required`: Add credits to account

**Google Cloud Errors:**
- `403 Forbidden`: Enable the Speech-to-Text API
- `400 Bad Request`: Check audio format (must be base64)
- `401 Unauthorized`: Verify credentials JSON

### Debug Commands:
```bash
# Check environment variables in Railway
railway variables

# View logs
railway logs

# Test locally first
cd backend
python -c "import os; print('OpenAI:', os.getenv('OPENAI_API_KEY')[:10] + '...')"
```

## ✅ Verification Checklist

- [ ] OpenAI API key added to Railway
- [ ] Google Cloud API key added to Railway  
- [ ] Google credentials JSON uploaded
- [ ] APIs enabled in Google Cloud Console
- [ ] Billing set up for both services
- [ ] Test endpoints return successful responses
- [ ] Usage monitoring configured

Once these are configured, your AI features will be fully functional!