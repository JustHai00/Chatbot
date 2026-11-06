@echo off
title 🔍 Debug SHADOW
cd /d "%~dp0"
echo ======================================
echo 🌑 Starting SHADOW (Debug Mode)...
echo ======================================
echo.

"C:\Users\sin hu hai\AppData\Local\Python\pythoncore-3.14-64\python.exe" -m streamlit run shadow.py --server.headless true

echo.
echo ======================================
echo ✅ Done — or ❌ error above?
echo ======================================
pause
