@echo off
:: Get the current username
for /f "tokens=2 delims==" %%A in ('wmic os get localname /value') do set "pcname=%%A"
for /f "tokens=2 delims==" %%A in ('wmic computersystem get username /value') do set "username=%%A"

:: Set source and destination paths
set "current_dir=%~dp0"
set "startup_dir=C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

:: Create destination directory if it doesn't exist
if not exist "%startup_dir%" mkdir "%startup_dir%"

:: Copy the launcher batch file to startup
copy "%current_dir%\run.bat" "%startup_dir%\" >nul

:: Create a temporary working directory
set "work_dir=C:\Users\%username%\AppData\Local\Temp\py_server"
if not exist "%work_dir%" mkdir "%work_dir%"

:: Copy all necessary files to working directory
xcopy "%current_dir%\server.py" "%work_dir%\" /Y >nul
xcopy "%current_dir%\requirements.txt" "%work_dir%\" /Y >nul
xcopy "%current_dir%\.env" "%work_dir%\" /Y >nul
xcopy "%current_dir%\serviceAccountKey.json" "%work_dir%\" /Y >nul

:: Create a separate launcher script in the working directory
(
echo @echo off
echo cd /d "%work_dir%"
echo python -m venv venv
echo call venv\Scripts\activate.bat
echo pip install --quiet --disable-pip-version-check -r requirements.txt
echo python server.py
) > "%work_dir%\start_server.bat"

:: Create a shortcut in Startup to launch the server
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%startup_dir%\PyServer.lnk');$s.TargetPath='%work_dir%\start_server.bat';$s.WorkingDirectory='%work_dir%';$s.WindowStyle=7;$s.Save()"

echo Server installation completed. It will start automatically on next login.
pause