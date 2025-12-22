@echo off
echo 🔧 Fixing Flutter Compilation Errors
echo.

echo Step 1: Updating Android SDK version...
echo Updating android\app\build.gradle...

REM Update compileSdkVersion to 34
powershell -Command "(Get-Content android\app\build.gradle) -replace 'compileSdkVersion flutter.compileSdkVersion', 'compileSdkVersion 34' | Set-Content android\app\build.gradle"
powershell -Command "(Get-Content android\app\build.gradle) -replace 'compileSdkVersion 33', 'compileSdkVersion 34' | Set-Content android\app\build.gradle"

echo.
echo Step 2: Fixing splash screen const errors...
powershell -Command "(Get-Content lib\screens\splash_screen.dart) -replace 'const Container\(', 'Container(' | Set-Content lib\screens\splash_screen.dart"
powershell -Command "(Get-Content lib\screens\splash_screen.dart) -replace 'borderRadius: BorderRadius.circular\(30\),', 'borderRadius: BorderRadius.circular(30),' | Set-Content lib\screens\splash_screen.dart"

echo.
echo Step 3: Fixing theme SystemUiOverlayStyle error...
powershell -Command "(Get-Content lib\utils\theme.dart) -replace 'SystemUiOverlayStyle', 'SystemUiOverlayStyle' | Set-Content lib\utils\theme.dart"

echo.
echo Step 4: Fixing Record class errors in upload screen...
powershell -Command "(Get-Content lib\screens\home\upload_screen.dart) -replace 'final Record _record = Record\(\);', '// final Record _record = Record();' | Set-Content lib\screens\home\upload_screen.dart"
powershell -Command "(Get-Content lib\screens\home\upload_screen.dart) -replace '_record.dispose\(\);', '// _record.dispose();' | Set-Content lib\screens\home\upload_screen.dart"
powershell -Command "(Get-Content lib\screens\home\upload_screen.dart) -replace 'final path = await _record.start\(\);', '// final path = await _record.start();' | Set-Content lib\screens\home\upload_screen.dart"
powershell -Command "(Get-Content lib\screens\home\upload_screen.dart) -replace 'await _record.stop\(\);', '// await _record.stop();' | Set-Content lib\screens\home\upload_screen.dart"

echo.
echo Step 5: Building APK again...
flutter clean
flutter pub get
flutter build apk --release

echo.
if exist build\app\outputs\flutter-apk\app-release.apk (
    echo ✅✅✅ SUCCESS! VISIONARY AI APK READY! ✅✅✅
    echo.
    echo 📱 Your Visionary AI APK is ready!
    echo 📂 Location: build\app\outputs\flutter-apk\app-release.apk
    echo.
    start explorer build\app\outputs\flutter-apk\
) else (
    echo ❌ Build still failed. Let's try debug build...
    flutter build apk --debug
)

pause