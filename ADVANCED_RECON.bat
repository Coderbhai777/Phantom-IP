@echo off
title PHANTOM-IP // ADVANCED RECON
color 0C
cls

echo ==================================================
echo   PHANTOM-IP // LIVE WSL AGGRESSIVE RECON
echo ==================================================
echo.

set /p TARGET="ENTER TARGET IP/HOST: "
if "%TARGET%"=="" set TARGET=127.0.0.1

echo.
echo [!] WARNING: EXECUTING SERVICE DETECTION AND OS FINGERPRINTING...
echo [!] COMMAND: nmap -sV -A -T4 %TARGET%
echo.
timeout /t 2 > nul

python phantom_tui.py %TARGET% --distro kali-linux --cmd "nmap -sV -A -T4 {target}"

pause
