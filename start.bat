@echo off
echo ==================================================
echo   Devil X Telegraph Bot
echo ==================================================

REM Load .env if it exists
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%A in (".env") do (
        set "line=%%A"
        if not "!line:~0,1!"=="#" (
            set "%%A=%%B"
        )
    )
    echo [INFO] Loaded .env file
)

echo [INFO] Starting bot...
python -m DevilxTelegraph
pause
