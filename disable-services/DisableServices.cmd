@echo off
setlocal enabledelayedexpansion

REM === Path to the service list file ===
set "SERVICE_LIST=%~dp0services.txt"

if not exist "%SERVICE_LIST%" (
    echo [ERROR] File not found: %SERVICE_LIST%
    pause
    exit /b
)

echo ================= Processing Services =================

for /f "usebackq tokens=*" %%s in ("%SERVICE_LIST%") do (
    set "SERVICE=%%s"
    if "!SERVICE!"=="" (
        REM Skip empty lines
        continue
    )

    echo.
    echo Processing service: !SERVICE!

    REM --- Get START_TYPE ---
    set "START_TYPE="
    for /f "tokens=3" %%a in ('sc qc "!SERVICE!" ^| findstr /i "START_TYPE"') do set "START_TYPE=%%a"

    if "!START_TYPE!"=="4" (
        echo [INFO] Service already disabled, skipping disable
    ) else (
        REM --- Disable service ---
        sc config "!SERVICE!" start= disabled >nul 2>&1
        if !errorlevel! equ 0 (
            echo [OK] Disabled service

            REM --- Check STATE only after successful disable ---
            set "STATE="
            for /f "tokens=3" %%r in ('sc query "!SERVICE!" ^| findstr /i "STATE"') do set "STATE=%%r"

            if "!STATE!"=="1" (
                echo [INFO] Service already stopped, skipping stop
            ) else (
                sc stop "!SERVICE!" >nul 2>&1
                if !errorlevel! equ 0 (
                    echo [OK] Service stopped
                ) else (
                    echo [FAIL] Could not stop service
                )
            )

        ) else (
            echo [FAIL] Could not disable service
        )
    )
)

echo.
echo --- [INFO] Finished processing service list.
pause
endlocal
