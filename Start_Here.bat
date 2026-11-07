@echo off
title 🌑 ECLIPSED
color 0B
cls
echo ==========================================
echo     🌑 ECLIPSED — Starting...
echo ==========================================
echo.

:: Go to where this file is
cd /d "%~dp0"

:: Check Python
echo [1/3] Checking Python...
"C:\Users\sin hu hai\AppData\Local\Python\pythoncore-3.14-64\python.exe" --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found at expected path!
    pause
    exit /b 1
)
echo ✅ Python found

:: Install tools if needed
echo [2/3] Checking required tools...
"C:\Users\sin hu hai\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m pip install streamlit PyPDF2 python-docx pandas openpyxl -q
echo ✅ Tools ready

:: Start ECLIPSED
echo [3/3] Opening ECLIPSED...
echo.
"C:\Users\sin hu hai\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run main_app.py --server.port 8888 --server.open_browser true

if errorlevel 1 (
    echo.
    echo ❌ Something went wrong
    pause
)
