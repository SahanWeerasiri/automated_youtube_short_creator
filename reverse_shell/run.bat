@echo off
:: run.bat - Manual setup script
:: This should be run manually once to set up the persistent server

:: Get current username
for /f "tokens=2 delims==" %%A in ('wmic computersystem get username /value 2^>nul') do set "username=%%A"

:: Set directories
set "current_dir=%~dp0"
set "work_dir=C:\Users\%username%\AppData\Local\Temp\py_server"
set "startup_dir=C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

:: Create working directory if it doesn't exist
if not exist "%work_dir%" mkdir "%work_dir%"

:: Copy all necessary files (except run.bat)
echo Copying files to working directory...
xcopy "%current_dir%\server.py" "%work_dir%\" /Y >nul
xcopy "%current_dir%\requirements.txt" "%work_dir%\" /Y >nul
if exist "%current_dir%\.env" xcopy "%current_dir%\.env" "%work_dir%\" /Y >nul
if exist "%current_dir%\serviceAccountKey.json" xcopy "%current_dir%\serviceAccountKey.json" "%work_dir%\" /Y >nul

:: Create the WiFi-checking launcher batch file
(
echo @echo off
echo :: Launcher script - waits for WiFi then starts server
echo setlocal enabledelayedexpansion
echo 
echo :CHECK_WIFI
echo echo [%date% %time%] Checking for internet connection...
echo ping -n 1 8.8.8.8 ^>nul 2^>^&1
echo if errorlevel 1 (
echo     echo [%date% %time%] No internet. Retrying in 30 seconds...
echo     timeout /t 30 /nobreak ^>nul
echo     goto CHECK_WIFI
echo )
echo 
echo :: First-time setup check
echo if not exist "venv\\" (
echo     echo [%date% %time%] Creating virtual environment...
echo     python -m venv venv
echo     call venv\Scripts\activate.bat
echo     echo [%date% %time%] Installing requirements...
echo     pip install --quiet --disable-pip-version-check -r requirements.txt
echo ) else (
echo     call venv\Scripts\activate.bat
echo )
echo 
echo :: Run server
echo echo [%date% %time%] Starting server...
echo python server.py
echo echo [%date% %time%] Server stopped or crashed. Restarting...
echo goto CHECK_WIFI
) > "%work_dir%\server_launcher.bat"

:: Create a VBS script to run hidden
(
echo Set WshShell = CreateObject("WScript.Shell"^)
echo WshShell.Run "cmd /c ""%work_dir%\server_launcher.bat""", 0, False
) > "%work_dir%\hidden_launcher.vbs"

:: Add to startup (only if not already there)
if not exist "%startup_dir%\PyServer.lnk" (
    echo Creating startup shortcut...
    powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%startup_dir%\PyServer.lnk');$s.TargetPath='wscript.exe';$s.Arguments='""%work_dir%\hidden_launcher.vbs""';$s.WorkingDirectory='%work_dir%';$s.WindowStyle=7;$s.Save()" >nul
)

echo Setup complete! The server will:
echo 1. Start automatically on system login (hidden)
echo 2. Wait for WiFi connection before starting
echo 3. Automatically set up virtual environment on first run
echo 4. Restart if the server crashes

pause