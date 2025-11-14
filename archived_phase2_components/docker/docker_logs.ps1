# ==========================================
# FIAE AI Content Factory - Docker Logs Viewer
# ==========================================

param(
    [string]$Service = "all"
)

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "📋 FIAE AI Content Factory - Docker Logs" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

if ($Service -eq "all") {
    Write-Host "📊 Showing logs for all services (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f
} elseif ($Service -eq "backend") {
    Write-Host "📊 Showing backend logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f backend
} elseif ($Service -eq "frontend") {
    Write-Host "📊 Showing frontend logs (Ctrl+C to exit)..." -ForegroundColor Yellow
    docker-compose logs -f frontend
} else {
    Write-Host "❌ Invalid service: $Service" -ForegroundColor Red
    Write-Host "   Valid options: all, backend, frontend" -ForegroundColor Yellow
}

