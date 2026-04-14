@echo off
title PHANTOM-IP // LIVE WSL SCANNER
color 0A
cls

echo ==================================================
echo   PHANTOM-IP // REAL-TIME WSL KALI BRIDGE
echo ==================================================
echo.

set /p TARGET="ENTER TARGET IP/HOST: "
if "%TARGET%"=="" set TARGET=127.0.0.1

echo.
echo [!] ATTEMPTING TO INITIALIZE KALI-LINUX VIA WSL...
echo [!] RUNNING: nmap -v -sT %TARGET%
echo.
timeout /t 2 > nul

python phantom_tui.py %TARGET% --distro kali-linux --cmd "nmap -v -sT {target}"

pause
