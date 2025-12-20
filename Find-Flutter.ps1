# Find Flutter Installation
Write-Host "🔍 Searching for Flutter on your system..." -ForegroundColor Cyan
Write-Host ""

# Check PATH first
Write-Host "Checking if Flutter is in PATH..." -ForegroundColor Yellow
$flutterInPath = Get-Command flutter -ErrorAction SilentlyContinue
if ($flutterInPath) {
    Write-Host "✅ Flutter found in PATH!" -ForegroundColor Green
    Write-Host "Location: $($flutterInPath.Source)" -ForegroundColor Green
    flutter --version
    exit 0
}

# Search common locations
Write-Host "Searching common installation directories..." -ForegroundColor Yellow
$commonPaths = @(
    "C:\flutter\bin\flutter.exe",
    "C:\src\flutter\bin\flutter.exe",
    "$env:USERPROFILE\flutter\bin\flutter.exe",
    "$env:USERPROFILE\Downloads\flutter\bin\flutter.exe",
    "$env:USERPROFILE\Desktop\flutter\bin\flutter.exe",
    "$env:LOCALAPPDATA\flutter\bin\flutter.exe",
    "C:\Program Files\flutter\bin\flutter.exe",
    "C:\tools\flutter\bin\flutter.exe"
)

$found = $false
foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        Write-Host "✅ FOUND: $path" -ForegroundColor Green
        & $path --version
        Write-Host ""
        Write-Host "To use Flutter, add this to your PATH:" -ForegroundColor Cyan
        Write-Host (Split-Path $path) -ForegroundColor White
        $found = $true
    }
}

if (-not $found) {
    Write-Host "Searching entire system (this may take a minute)..." -ForegroundColor Yellow
    $results = Get-ChildItem -Path C:\ -Filter flutter.exe -Recurse -ErrorAction SilentlyContinue | Select-Object -First 5
    
    if ($results) {
        Write-Host "✅ Found Flutter installations:" -ForegroundColor Green
        foreach ($result in $results) {
            Write-Host $result.FullName -ForegroundColor White
        }
    } else {
        Write-Host "❌ Flutter not found on your system" -ForegroundColor Red
        Write-Host ""
        Write-Host "Download Flutter from: https://flutter.dev/docs/get-started/install/windows" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")