@echo off
REM Contributor setup script for Windows
setlocal enabledelayedexpansion

echo CDISC Rules Engine - Contributor Setup
echo.

REM Warn if not running as admin
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
    winget install Python.Python.3.12 --silent --accept-source-agreements
    if !errorlevel! equ 0 goto :refresh_and_verify
)

REM Try chocolatey
where choco >nul 2>&1
if !errorlevel! equ 0 (
    echo Installing Python 3.12 via Chocolatey...
    choco install python312 -y
    if !errorlevel! equ 0 goto :refresh_and_verify
)

REM Direct download and install as last resort
echo Downloading Python 3.12 installer...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.8/python-3.12.8-amd64.exe' -OutFile '%TEMP%\py312.exe'"
%TEMP%\py312.exe /quiet InstallAllUsers=1 PrependPath=1
del "%TEMP%\py312.exe"

:refresh_and_verify
REM Combine system and user paths for the current session
for /f "tokens=2*" %%a in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%b"
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USR_PATH=%%b"
set "PATH=%SYS_PATH%;%USR_PATH%"

set "PYTHON_CMD=python"

:setup_venv
echo.
echo Setting up virtual environment...
if exist "venv\" rmdir /s /q venv
!PYTHON_CMD! -m venv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip setuptools wheel --quiet
python -m pip install -r engine\requirements.txt --quiet
python -m pip install -r engine\requirements-dev.txt --quiet

echo.
echo Setup completed successfully!
pause