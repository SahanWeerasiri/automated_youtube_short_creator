@echo off

:: Get current username (most reliable method)
set "username=%USERNAME%"

:: Set directories
set "work_dir=C:\Users\%username%\AppData\Local\Temp\py_server"

:: Change directory (with error checking)
if not exist "%work_dir%" (
    echo Error: Working directory does not exist: %work_dir%
    pause
    exit /b 1
)
cd /d "%work_dir%"

:: Launcher script - waits for WiFi then starts server
setlocal enabledelayedexpansion

:CHECK_WIFI
echo [%date% %time%] Checking for internet connection...
ping -n 1 8.8.8.8 >nul 2>&1
if errorlevel 1 (
    echo [%date% %time%] No internet. Retrying in 30 seconds...
    timeout /t 30 /nobreak >nul
    goto CHECK_WIFI
)

:: First-time setup check
if not exist "venv\" (
    echo [%date% %time%] Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [%date% %time%] Installing requirements...
    pip install --quiet --disable-pip-version-check -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

:: Run server
echo [%date% %time%] Starting server...
python server.py
echo [%date% %time%] Server stopped or crashed. Restarting...
goto CHECK_WIFI
