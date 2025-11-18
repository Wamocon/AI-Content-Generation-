# ==========================================
# FIAE AI Content Factory - Docker System Startup
# ==========================================

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "🚀 FIAE AI Content Factory - Docker Startup" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "🔍 Checking Docker status..." -ForegroundColor Yellow
try {
    $dockerInfo = docker info 2>&1 | Select-String "Server Version"
    if (-not $dockerInfo) {
        throw "Docker not running"
    }
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop." -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 1
}

Write-Host ""

# Check if .env file exists
Write-Host "🔍 Checking for .env file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Write-Host "❌ .env file not found!" -ForegroundColor Red
    Write-Host "   Please copy env.example to .env and configure your credentials" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 1
}
Write-Host "✅ .env file found" -ForegroundColor Green

Write-Host ""

# Stop any existing containers
Write-Host "🔧 Stopping existing containers..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null
Write-Host "✅ Existing containers stopped" -ForegroundColor Green

Write-Host ""

# Build and start containers
Write-Host "🏗️  Building Docker containers..." -ForegroundColor Cyan
Write-Host "   This may take several minutes on first build..." -ForegroundColor Gray
Write-Host ""

docker-compose build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker build failed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 1
}

Write-Host ""
Write-Host "✅ Containers built successfully" -ForegroundColor Green

Write-Host ""

# Start containers
Write-Host "🚀 Starting containers..." -ForegroundColor Cyan
docker-compose up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start containers!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
    exit 1
}

Write-Host "✅ Containers started successfully" -ForegroundColor Green

Write-Host ""

# Wait for services to be ready
Write-Host "⏳ Waiting for services to initialize..." -ForegroundColor Yellow
Write-Host "   Backend starting (30 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 30

# Check backend health
Write-Host "🔍 Checking backend health..." -ForegroundColor Yellow
$retries = 0
$maxRetries = 10
$backendHealthy = $false

while ($retries -lt $maxRetries -and -not $backendHealthy) {
    try {
        $healthResponse = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method GET -TimeoutSec 5 -ErrorAction Stop
        if ($healthResponse.status -eq "healthy") {
            $backendHealthy = $true
            Write-Host "✅ Backend is healthy!" -ForegroundColor Green
            Write-Host "   Status: $($healthResponse.status)" -ForegroundColor Green
            Write-Host "   Version: $($healthResponse.version)" -ForegroundColor Green
        }
    } catch {
        $retries++
        if ($retries -lt $maxRetries) {
            Write-Host "   Attempt $retries/$maxRetries - waiting..." -ForegroundColor Gray
            Start-Sleep -Seconds 3
        }
    }
}

if (-not $backendHealthy) {
    Write-Host "⚠️  Backend health check failed, but containers are running" -ForegroundColor Yellow
    Write-Host "   Check logs: docker-compose logs backend" -ForegroundColor Yellow
}

Write-Host ""

# Check frontend
Write-Host "🔍 Checking frontend..." -ForegroundColor Yellow
Start-Sleep -Seconds 10
try {
    $frontendResponse = Invoke-WebRequest -Uri "http://localhost:3000" -Method GET -TimeoutSec 5 -ErrorAction Stop
    Write-Host "✅ Frontend is running!" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Frontend may still be starting..." -ForegroundColor Yellow
    Write-Host "   Check logs: docker-compose logs frontend" -ForegroundColor Yellow
}

Write-Host ""

# Display system status
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "📊 SYSTEM STATUS" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "🌐 ACCESS INFORMATION" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   Frontend:    http://localhost:3000" -ForegroundColor Green
Write-Host "   Backend:     http://localhost:8000" -ForegroundColor Green
Write-Host "   API Docs:    http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "🔧 USEFUL COMMANDS" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "   View all logs:      docker-compose logs -f" -ForegroundColor White
Write-Host "   View backend logs:  docker-compose logs -f backend" -ForegroundColor White
Write-Host "   View frontend logs: docker-compose logs -f frontend" -ForegroundColor White
Write-Host "   Stop system:        docker-compose down" -ForegroundColor White
Write-Host "   Restart system:     docker-compose restart" -ForegroundColor White
Write-Host ""

Write-Host "✅ FIAE AI Content Factory is ready!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to open the application in your browser..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Open application in browser
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "✅ Application opened in browser!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit (containers will continue running)..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

