@echo off
echo Fixing Android SDK version issue...

REM Create a fixed build.gradle content
echo Creating fixed build.gradle...

(
echo plugins {
echo     id "com.android.application"
echo     id "kotlin-android"
echo     id "dev.flutter.flutter-gradle-plugin"
echo }
echo.
echo def localProperties = new Properties^(^)
echo def localPropertiesFile = rootProject.file^('local.properties'^)
echo if ^(localPropertiesFile.exists^(^)^) {
echo     localPropertiesFile.withReader^('UTF-8'^) { reader -^>
echo         localProperties.load^(reader^)
echo     }
echo }
echo.
echo def flutterVersionCode = localProperties.getProperty^('flutter.versionCode'^)
echo if ^(flutterVersionCode == null^) {
echo     flutterVersionCode = '1'
echo }
echo.
echo def flutterVersionName = localProperties.getProperty^('flutter.versionName'^)
echo if ^(flutterVersionName == null^) {
echo     flutterVersionName = '1.0'
echo }
echo.
echo android {
echo     namespace "com.example.visionary_mobile_fresh"
echo     compileSdkVersion flutter.compileSdkVersion
echo     ndkVersion flutter.ndkVersion
echo.
echo     compileOptions {
echo         sourceCompatibility JavaVersion.VERSION_1_8
echo         targetCompatibility JavaVersion.VERSION_1_8
echo     }
echo.
echo     kotlinOptions {
echo         jvmTarget = '1.8'
echo     }
echo.
echo     sourceSets {
echo         main.java.srcDirs += 'src/main/kotlin'
echo     }
echo.
echo     defaultConfig {
echo         applicationId "com.example.visionary_mobile_fresh"
echo         minSdkVersion 21
echo         targetSdkVersion flutter.targetSdkVersion
echo         versionCode flutterVersionCode.toInteger^(^)
echo         versionName flutterVersionName
echo     }
echo.
echo     buildTypes {
echo         release {
echo             signingConfig signingConfigs.debug
echo         }
echo     }
echo }
echo.
echo flutter {
echo     source '../..'
echo }
echo.
echo dependencies {}
) > "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh\android\app\build.gradle"

echo build.gradle updated successfully!

echo.
echo Now building the app with fixed SDK version...
cd /d "C:\Users\Martin Mbugua\Desktop\visionary_mobile_fresh"
flutter clean
flutter pub get
flutter build apk --debug

echo.
echo Build completed!
pause