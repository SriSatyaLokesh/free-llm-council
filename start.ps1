# Free LLM Council - Windows PowerShell Startup Script

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " Free LLM Council - Startup Script" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[*] Ensuring OpenCode service is running..." -ForegroundColor Yellow
python -c "from backend.opencode_client import ensure_opencode_running; ensure_opencode_running()"

Write-Host "[*] Starting Backend server (http://localhost:8001)..." -ForegroundColor Yellow
$backend = Start-Process python -ArgumentList "-m backend.main" -PassThru

Start-Sleep -Seconds 2

Write-Host "[*] Starting Frontend server (http://localhost:5173)..." -ForegroundColor Yellow
$frontend = Start-Process npm -ArgumentList "run dev" -WorkingDirectory "frontend" -PassThru

Write-Host ""
Write-Host "========================================================" -ForegroundColor Green
Write-Host " [+] LLM Council is running!" -ForegroundColor Green
Write-Host "   - Frontend: http://localhost:5173" -ForegroundColor Green
Write-Host "   - Backend:  http://localhost:8001" -ForegroundColor Green
Write-Host "========================================================" -ForegroundColor Green
Write-Host ""
