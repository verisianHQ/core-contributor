@echo off
REM Contributor setup script for Windows
setlocal enabledelayedexpansion

echo CDISC Rules Engine - Contributor Setup
echo.

REM Check for Python 3.12+
set "PYTHON_CMD="
set "REQUIRED_VERSION=3.12"

where python3.12 >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=2" %%v in ('python3.12 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    echo Found python3.12: !PYTHON_VERSION!
    set "PYTHON_CMD=python3.12"
    goto :python_found
)

where python3 >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=2" %%v in ('python3 --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    for /f "delims=. tokens=1,2" %%a in ("!PYTHON_VERSION!") do (
        if %%a GEQ 3 if %%b GEQ 12 (
            echo Found python3: !PYTHON_VERSION!
            set "PYTHON_CMD=python3"
            goto :python_found
        )
    )
)

where python >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
    for /f "delims=. tokens=1,2" %%a in ("!PYTHON_VERSION!") do (
        if %%a GEQ 3 if %%b GEQ 12 (
            echo Found python: !PYTHON_VERSION!
            set "PYTHON_CMD=python"
            goto :python_found
        )
    )
)

echo Python 3.12 not found. Installing automatically...
echo.

REM Try winget first (Windows 10 1809+ and Windows 11)
where winget >nul 2>&1
if !errorlevel! equ 0 (
    echo Installing Python 3.12 via winget...
    winget install Python.Python.3.12 --silent --accept-source-agreements --accept-package-agreements
    if !errorlevel! equ 0 (
        echo Python 3.12 installed successfully
        echo Refreshing environment...
        call refreshenv >nul 2>&1
        set "PYTHON_CMD=python3.12"
        goto :python_found
    )
)

REM Try chocolatey if available
where choco >nul 2>&1
if !errorlevel! equ 0 (
    echo Installing Python 3.12 via Chocolatey...
    choco install python312 -y
    if !errorlevel! equ 0 (
        echo Python 3.12 installed successfully
        echo Refreshing environment...
        call refreshenv >nul 2>&1
        set "PYTHON_CMD=python3.12"
        goto :python_found
    )
)

REM Direct download and install as last resort
echo Downloading Python 3.12 installer...
set "PYTHON_INSTALLER=%TEMP%\python-3.12-installer.exe"
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe' -OutFile '%PYTHON_INSTALLER%'"

if !errorlevel! neq 0 (
    echo Failed to download Python installer
    echo Please install Python 3.12 manually from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing Python 3.12...
%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
if !errorlevel! neq 0 (
    echo Python installation failed
    del "%PYTHON_INSTALLER%"
    pause
    exit /b 1
)

del "%PYTHON_INSTALLER%"
echo Python 3.12 installed successfully

REM Refresh PATH
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path') do set "NEW_PATH=%%b"
set "PATH=%NEW_PATH%"

REM Try to find Python again
where python3.12 >nul 2>&1
if !errorlevel! equ 0 (
    set "PYTHON_CMD=python3.12"
) else (
    where python >nul 2>&1
    if !errorlevel! equ 0 (
        set "PYTHON_CMD=python"
    ) else (
        echo Python installation succeeded but command not found in PATH
        echo Please restart your terminal and run this script again
        pause
        exit /b 1
    )
)

:python_found

echo.
echo Setting up virtual environment...
cd engine

if exist "venv\" (
    if not exist "venv\Scripts\activate.bat" (
        echo Removing broken virtual environment...
        rmdir /s /q venv
    )
)

if not exist "venv\" (
    echo Creating virtual environment...
    %PYTHON_CMD% -m venv venv
    if !errorlevel! neq 0 (
        echo Failed to create virtual environment
        cd ..
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if !errorlevel! neq 0 (
    echo Failed to activate virtual environment
    cd ..
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
python -m pip install --upgrade pip --quiet

if not exist "requirements.txt" (
    echo requirements.txt not found in engine directory
    cd ..
    pause
    exit /b 1
)

pip install -r requirements.txt --quiet
if !errorlevel! neq 0 (
    echo Failed to install dependencies
    cd ..
    pause
    exit /b 1
)

if not exist "requirements-dev.txt" (
    echo requirements-dev.txt not found in engine directory
    cd ..
    pause
    exit /b 1
)

pip install -r requirements-dev.txt --quiet
if !errorlevel! neq 0 (
    echo Failed to install dependencies
    cd ..
    pause
    exit /b 1
)

cd ..

echo.
echo Setup completed successfully!
pause