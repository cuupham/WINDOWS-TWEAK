@echo off
setlocal enabledelayedexpansion

REM === Configure path to the service list file ===
set "SERVICE_LIST=%~dp0services_list.txt"

REM === Check if file exists ===
if not exist "%SERVICE_LIST%" (
    echo [ERROR] File not found: %SERVICE_LIST%
    pause
    exit /b
)

REM === Process each service ===
for /f %%s in (%SERVICE_LIST%) do (
    echo.
    echo Disabling service: %%s

    sc config %%s start= disabled >nul 2>&1
    if !errorlevel! equ 0 (
        echo [OK] Successfully set to disabled
    ) else (
        echo [FAIL] Failed to change startup type
    )

    sc stop %%s >nul 2>&1
    if !errorlevel! equ 0 (
        echo [OK] Service stopped
    ) else (
        echo [FAIL] Could not stop service (maybe already stopped^)
    )
)

echo.
echo --- [INFO] Finished processing service list.
pause
endlocal
