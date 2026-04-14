@echo off
title PHANTOM-IP // AGGRESSIVE MODE
color 0C
cls
echo [!] WARNING: ENTERING AGGRESSIVE BREACH MODE...
echo [!] OVERRIDING KERNEL PRIVILEGES...
timeout /t 2 /nobreak > nul

set TARGET=%1
if "%TARGET%"=="" set TARGET=192.168.1.1

python phantom_tui.py %TARGET% --hack

pause
