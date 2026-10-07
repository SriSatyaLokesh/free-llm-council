@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo  Free LLM Council - Startup Script
echo ========================================================
echo.

echo [*] Ensuring OpenCode background service is running...
python -c "from backend.opencode_client import ensure_opencode_running; ensure_opencode_running()"

echo [*] Starting LLM Council Backend on http://localhost:8001...
start "LLM Council Backend" cmd /c "python -m backend.main"

timeout /t 2 /nobreak >nul

echo [*] Starting LLM Council Frontend on http://localhost:5173...
cd frontend
start "LLM Council Frontend" cmd /c "npm run dev"
cd ..

echo.
echo ========================================================
echo  [+] LLM Council is running!
echo    - Frontend: http://localhost:5173
echo    - Backend:  http://localhost:8001
echo ========================================================
echo.
pause
