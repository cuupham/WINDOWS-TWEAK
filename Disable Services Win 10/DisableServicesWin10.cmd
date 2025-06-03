@echo off
for /f %%s in (win_10_disabled_services.txt) do (
    echo Disabling service: %%s
    sc config %%s start= disabled
    sc stop %%s
)
echo Done.
pause
