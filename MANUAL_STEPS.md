# Manual Steps to Fix and Build

If the batch files are closing too fast, follow these manual steps:

## Step 1: Replace API Service
```bash
cd mobile_app
copy src\services\api-fetch.ts src\services\api.ts
```

## Step 2: Remove Axios
```bash
npm uninstall axios
```

## Step 3: Build
```bash
eas build --platform android --profile preview
```

That's it! The build will run on EAS cloud servers for 10-15 minutes.

## What This Does
- Removes axios (causes crypto errors)
- Uses native fetch instead (built into React Native)
- No more Node.js dependency issues
- Smaller, faster app

## Check Build Status
https://expo.dev/accounts/martinmbugua/projects/visionary-ai-scheduler/builds

## If You Get Errors
The most common issue is the api-fetch.ts file not being in the right place. Make sure:
- You're in the `mobile_app` folder
- The file `src/services/api-fetch.ts` exists
- Then copy it to `src/services/api.ts`
