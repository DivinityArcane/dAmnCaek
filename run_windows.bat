@echo off
cls
echo Trying to launch the server, you should have Python 3 installed as your default "python" executable.

:start
python main.py
echo ================ Execution has halted. 

:ask
set /P redo=Restart? [y/n]:%redo%
if %redo%==y (
    goto start
) else (
    goto stop
)

:stop
pause