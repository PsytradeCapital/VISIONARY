# Flutter Setup Help for Visionary AI

## The Problem
Flutter is installed on your system but not in your PATH, so Windows can't find it.

## Quick Solutions

### Option 1: Find Your Flutter Installation
Run this in PowerShell:
```powershell
Get-ChildItem -Path C:\, D:\, E:\ -Filter flutter.exe -Recurse -ErrorAction SilentlyContinue | Select-Object FullName
```

### Option 2: Add Flutter to PATH Permanently

1. **Find Flutter location** - Check these common places:
   - `C:\flutter\bin`
   - `C:\src\flutter\bin`
   - `%USERPROFILE%\flutter\bin`
   - Your Downloads folder

2. **Add to PATH**:
   - Press `Win + X` → System
   - Click "Advanced system settings"
   - Click "Environment Variables"
   - Under "User variables", select "Path" → Edit
   - Click "New" → Add your Flutter bin path (e.g., `C:\flutter\bin`)
   - Click OK on all windows
   - **Restart your terminal/IDE**

### Option 3: Fresh Flutter Install

1. Download Flutter:
   ```
   https://docs.flutter.dev/get-started/install/windows
   ```

2. Extract to `C:\flutter`

3. Add `C:\flutter\bin` to PATH (see Option 2)

4. Verify:
   ```cmd
   flutter doctor
   ```

### Option 4: Use Chocolatey (Easiest!)

If you have Chocolatey installed:
```cmd
choco install flutter
```

## After Flutter is Working

Run our app creator:
```cmd
create_flutter_app.bat
```

Or use the updated version:
```cmd
flutter_installer.bat
```

## Still Having Issues?

Tell me where Flutter is installed, and I'll create a custom script for your specific path!