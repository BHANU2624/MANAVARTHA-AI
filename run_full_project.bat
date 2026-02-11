@echo off
echo ===================================================
echo   MANA VARTHA AI - Launcher
echo ===================================================
echo.

echo [1/2] Starting Backend Server...
cd backend
start "MANAVARTHA Backend" start.bat
cd ..

echo [2/2] Launching Flutter App...
cd telugu_news_app
echo If this is your first time, it might take a minute to compile.
call flutter run -d windows

echo.
echo Application Closed.
pause
