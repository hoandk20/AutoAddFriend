@echo off
:: Check if the script is run as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    :: Run the Python script
    python "C:\Users\k\OneDrive\Desktop\Code\AutoAddFriend\main.py"
) else (
    :: Request administrative privileges and rerun the batch file
    echo Requesting administrative privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c %~dp0%~nx0' -Verb RunAs"
)