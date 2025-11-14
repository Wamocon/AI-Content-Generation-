# ==========================================
# FIAE AI Content Factory - Docker System Stop
# ==========================================

Write-Host "===========================================" -ForegroundColor Cyan
Write-Host "🛑 FIAE AI Content Factory - Stopping Docker" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🔧 Stopping all containers..." -ForegroundColor Yellow
docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All containers stopped successfully" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some containers may still be running" -ForegroundColor Yellow
    Write-Host "   Run: docker ps -a" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

