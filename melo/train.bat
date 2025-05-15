@echo off
setlocal enabledelayedexpansion

:: Set Python encoding environment variables
set PYTHONIOENCODING=utf-8
set PYTHONLEGACYWINDOWSSTDIO=utf-8

:: Set the relative path to the config file as a parameter
set "RELATIVE_CONFIG_PATH=data\example\config.json"

:: Get the directory of the batch file
set "SCRIPT_DIR=%~dp0"

:: Construct the full path to the config file
set "CONFIG=%SCRIPT_DIR%%RELATIVE_CONFIG_PATH%"

:: Extract the model name from the config path
for %%F in ("%CONFIG%") do set "MODEL_NAME=%%~dpnF"

:: Ask user about G model preference
echo Do you want to use:
echo 1. Default G model
echo 2. Custom G model
set /p MODEL_CHOICE="Enter your choice (1 or 2): "

if "%MODEL_CHOICE%"=="2" (
    set /p G_MODEL_PATH="Enter the path to your G model file: "
    set "G_MODEL_ARG=--pretrain_G "%G_MODEL_PATH%""
) else (
    set "G_MODEL_ARG="
)

:loop
python train.py -c "%CONFIG%" -m "%MODEL_NAME%" %G_MODEL_ARG%
for /f "tokens=2" %%a in ('tasklist ^| findstr python') do (
    taskkill /F /PID %%a
)
timeout /t 30
goto loop