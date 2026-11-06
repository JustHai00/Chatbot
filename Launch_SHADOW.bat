@echo off
title 🌑 SHADOW — Your Personal AI
color 0A
echo ======================================
echo 🌑 SHADOW is starting...
echo ======================================
echo.

:: Go to your folder
cd /d "%~dp0"

:: Check Ollama running
tasklist | findstr /i "ollama.exe" >nul
if errorlevel 1 (
    echo ⚠️ Ollama not running — starting it now...
    start "" ollama serve
    timeout /t 3 /nobreak >nul
)

:: Launch SHADOW with your Python path
"C:\Users\sin hu hai\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run shadow.py --server.headless false

if errorlevel 1 (
    echo.
    echo ❌ Something went wrong — check above
    pause
)
