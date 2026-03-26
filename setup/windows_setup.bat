@echo off
REM Contributor setup script for Windows
setlocal enabledelayedexpansion

echo CDISC Rules Engine - Contributor Setup
echo.

REM Warn if not running as admin
net session >nul 2>&1
if !errorlevel! neq 0 (
    echo [WARNING] You are not running as Administrator. 
    echo If Python needs to be installed, the installation steps may fail.
    echo.
)

REM Check for Python 3.12.x
set "PYTHON_CMD="
set "REQUIRED_VERSION=3.12"

where python3.12 >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=2" %%v in ('python3.12 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Found python3.12: !PYTHON_VERSION!
    set "PYTHON_CMD=python3.12"
    goto :setup_venv
)

where python3 >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=2" %%v in ('python3 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    for /f "delims=. tokens=1,2" %%a in ("!PYTHON_VERSION!") do (
        if %%a EQU 3 if %%b EQU 12 (
            echo Found python3: !PYTHON_VERSION!
            set "PYTHON_CMD=python3"
            goto :setup_venv
        )
    )
)

where python >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    for /f "delims=. tokens=1,2" %%a in ("!PYTHON_VERSION!") do (
        if %%a EQU 3 if %%b EQU 12 (
            echo Found python: !PYTHON_VERSION!
            set "PYTHON_CMD=python"
            goto :setup_venv
        )
    )
)

echo Python 3.12 not found. Attempting automatic installation...
echo.

REM Try winget first (Windows 10 1809+ and Windows 11)
where winget >nul 2>&1
if !errorlevel! equ 0 (
    echo Installing Python 3.12 via winget...
    winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
    if !errorlevel! equ 0 (
        echo Python 3.12 installed successfully via winget.
        goto :refresh_and_verify
    )
)

REM Try chocolatey if available
where choco >nul 2>&1
if !errorlevel! equ 0 (
    echo Installing Python 3.12 via Chocolatey...
    choco install python312 -y
    if !errorlevel! equ 0 (
        echo Python 3.12 installed successfully via Chocolatey.
        goto :refresh_and_verify
    )
)

REM Direct download and install as last resort
echo Downloading Python 3.12 installer...
set "PYTHON_INSTALLER=%TEMP%\python-3.12-installer.exe"
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe' -OutFile '%PYTHON_INSTALLER%'"

if !errorlevel! neq 0 (
    echo Failed to download Python installer.
    echo Please install Python 3.12 manually from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing Python 3.12...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if !errorlevel! neq 0 (
    echo Python installation failed.
    del "%PYTHON_INSTALLER%"
    pause
    exit /b 1
)

del "%PYTHON_INSTALLER%"
echo Python 3.12 installed successfully via direct download.

:refresh_and_verify
REM Combine system and user paths for the current session
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USR_PATH=%%b"
set "PATH=%SYS_PATH%;%USR_PATH%"

REM Try to find Python again
where python3.12 >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python3.12"
    goto :setup_venv
) 

where python >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python"
    goto :setup_venv
)

echo.
echo Python was installed, but the command is not available in the current PATH.
echo Please restart your terminal and run this script again.
pause
exit /b 1


:setup_venv
echo.
echo Setting up virtual environment using !PYTHON_CMD!...

if exist "venv\" (
    echo Removing existing virtual environment...
    rmdir /s /q venv
)

if not exist "venv\" (
    echo Creating virtual environment...
    !PYTHON_CMD! -m venv venv
    if !errorlevel! neq 0 (
        echo Failed to create virtual environment.
        cd ..
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo Failed to activate virtual environment.
    cd ..
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
python -m pip install --upgrade pip setuptools wheel --quiet

if not exist "engine\requirements.txt" (
    echo requirements.txt not found in engine directory.
    pause
    exit /b 1
)

python -m pip install -r engine\requirements.txt --quiet
if !errorlevel! neq 0 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

if not exist "engine\requirements-dev.txt" (
    echo requirements-dev.txt not found in engine directory.
    pause
    exit /b 1
)

python -m pip install -r engine\requirements-dev.txt --quiet
if !errorlevel! neq 0 (
    echo Failed to install dev dependencies.
    pause
    exit /b 1
)

echo.
echo Setup completed successfully!
pause