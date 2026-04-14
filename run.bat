@echo off
title PHANTOM-IP // RED TEAM SUITE
color 0A
cls
echo [!] INITIALIZING PHANTOM SUBSYSTEM...
echo [!] CONNECTING TO WSL: KALI_LINUX...
timeout /t 2 /nobreak > nul

:: Check if rich is installed, if not try to install it
python -c "import rich" 2>nul
if %errorlevel% neq 0 (
    echo [!] DEPENDENCY 'RICH' NOT FOUND. INSTALLING...
    pip install rich
)

:: Run the TUI
python phantom_tui.py %*

pause
