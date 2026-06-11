@echo off
REM Contributor setup script for Windows
setlocal enabledelayedexpansion

echo CDISC Rules Engine - Contributor Setup
echo.

REM Warn if not running as admin [cite: 2]
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo Requesting Administrative privileges...
    powershell -Command "Start-Process -FilePath '%0' -Verb RunAs"
    exit /b
)

if exist "C:\ProgramData\chocolatey\lib-bad" (
    echo Cleaning up corrupted Chocolatey folders...
    rmdir /s /q "C:\ProgramData\chocolatey\lib-bad" >nul 2>&1
)

set "REQUIRED_VERSION=3.12"
set "PYTHON_CMD="

echo Checking for Python %REQUIRED_VERSION%...

REM 1. Try Windows Python Launcher (Safest and most reliable)
py -3.12 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python 3.12 via Windows Launcher.
    set "PYTHON_CMD=py -3.12"
    goto :setup_venv
)

REM 2. Try explicit python3.12 command
where python3.12 >nul 2>&1
if %errorlevel% equ 0 (
    echo Found python3.12 executable.
    set "PYTHON_CMD=python3.12"
    goto :setup_venv
)

REM 3. Try default python and verify version
where python >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    for /f "delims=. tokens=1,2" %%a in ("!PYTHON_VERSION!") do (
        if "%%a"=="3" if "%%b"=="12" (
            echo Found Python 3.12 as default python.
            set "PYTHON_CMD=python"
            goto :setup_venv
        )
    )
)

echo.
echo Python 3.12 not found. Attempting automatic installation... [cite: 6]
echo.

REM Try winget first (Windows 10 1809+ and Windows 11) [cite: 7]
where winget >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing Python 3.12 via winget...
    winget install Python.Python.3.12 --silent --accept-source-agreements
    
    REM Check if successful or already installed
    py -3.12 --version >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=py -3.12"
        goto :refresh_and_verify
    )
)

REM Try chocolatey [cite: 8]
where choco >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing Python 3.12 via Chocolatey...
    choco install python312 -y
    
    REM Check if successful
    py -3.12 --version >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=py -3.12"
        goto :refresh_and_verify
    )
)

REM Direct download and install as last resort
echo Downloading Python 3.12 installer...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe' -OutFile '%TEMP%\py312.exe'"
%TEMP%\py312.exe /quiet InstallAllUsers=1 PrependPath=1
del "%TEMP%\py312.exe"

set "PYTHON_CMD=py -3.12"

:refresh_and_verify
REM Combine system and user paths for the current session
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USR_PATH=%%b"
set "PATH=%SYS_PATH%;%USR_PATH%"

:setup_venv
echo.
echo Setting up virtual environment... [cite: 9]
if exist "venv\" rmdir /s /q venv

%PYTHON_CMD% -m venv venv [cite: 10]

call venv\Scripts\activate.bat

echo Installing dependencies...
venv\Scripts\python.exe -m pip install --upgrade pip setuptools wheel --quiet
venv\Scripts\python.exe -m pip install -r engine\requirements.txt --quiet
venv\Scripts\python.exe -m pip install -r engine\requirements-dev.txt --quiet

echo.
echo Setup completed successfully! [cite: 11]
pause