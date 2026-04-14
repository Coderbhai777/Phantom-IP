@echo off
setlocal
:: PhantomIP Global Wrapper (Sequential Version)

set SCRIPT_DIR=%~dp0

:: Pass arguments directly to the CLI script
:: Usage: PhantomIP [mode] --ip [target]
python "%SCRIPT_DIR%phantom_cli.py" %*

endlocal
