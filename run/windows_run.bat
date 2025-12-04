@echo off
setlocal enabledelayedexpansion

REM change to parent directory
cd /d "%~dp0\.."

REM Check if venv folder exists
if not exist "venv\" (
    echo Virtual environment not found. Running setup...
    call setup\windows_setup.bat
    if errorlevel 1 (
        echo Setup failed. Exiting.
        exit /b 1
    )
)

REM Check if python.exe exists in venv
if not exist "venv\Scripts\python.exe" (
    echo Python executable not found in virtual environment. Running setup...
    call setup\windows_setup.bat
    if errorlevel 1 (
        echo Setup failed. Exiting.
        exit /b 1
    )
)

REM Activate venv and run test.py
call venv\Scripts\activate.bat
echo Running test.py...
python test.py

endlocal
pause