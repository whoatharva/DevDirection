@echo off
SETLOCAL EnableDelayedExpansion

:: Check if virtual environment exists
IF NOT EXIST .venv (
    echo [INFO] Virtual environment not found. Creating .venv...
    python -m venv .venv
    IF !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Failed to create virtual environment. Please ensure Python is installed.
        pause
        exit /b !ERRORLEVEL!
    )
    
    echo [INFO] Installing dependencies...
    .venv\Scripts\python -m pip install --upgrade pip
    .venv\Scripts\python -m pip install -r requirements.txt
    IF !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Failed to install dependencies.
        pause
        exit /b !ERRORLEVEL!
    )
)

echo [INFO] Starting Career Guidance Platform...
echo [INFO] The dashboard will open automatically in your browser.
echo [INFO] Access the UI at http://127.0.0.1:8000/ui

:: Open the browser in the background after 2 seconds
start "" powershell -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:8000/ui'"

:: Start the server
.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

IF !ERRORLEVEL! NEQ 0 (
    echo [ERROR] Application crashed or failed to start.
    pause
)
