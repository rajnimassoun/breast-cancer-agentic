@echo off
REM ============================================================
REM Breast Cancer Agentic ML - Quick Launcher (Windows)
REM ============================================================
REM This batch file provides quick access to common operations
REM ============================================================

setlocal

echo.
echo ========================================================================
echo             BREAST CANCER AGENTIC ML - QUICK LAUNCHER
echo ========================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if main.py exists
if not exist "main.py" (
    echo ERROR: main.py not found in current directory
    echo Please run this script from the project root
    pause
    exit /b 1
)

:MENU
cls
echo.
echo ========================================================================
echo             BREAST CANCER AGENTIC ML - QUICK LAUNCHER
echo ========================================================================
echo.
echo Select an option:
echo.
echo   [1] Run Full ML Pipeline (Interactive)
echo   [2] Run Full ML Pipeline (Non-Interactive)
echo   [3] Run Agent Pipeline - All Stages
echo   [4] Run Agent Pipeline - EDA Only
echo   [5] Run Agent Pipeline - Modeling Only
echo   [6] Run Agent Pipeline - Explanation Only
echo   [7] Run Jupyter Notebooks (00_eda, 01_eda, etc.)
echo   [8] Run Quick Test
echo   [9] Interactive Menu (Python)
echo   [A] View Help
echo   [0] Exit
echo.
echo ========================================================================
echo.

set /p choice="Enter your choice (0-9, A): "

if "%choice%"=="0" goto EXIT
if "%choice%"=="1" goto FULL_INTERACTIVE
if "%choice%"=="2" goto FULL_BATCH
if "%choice%"=="3" goto AGENTS_ALL
if "%choice%"=="4" goto AGENTS_EDA
if "%choice%"=="5" goto AGENTS_MODELING
if "%choice%"=="6" goto AGENTS_EXPLAIN
if "%choice%"=="7" goto NOTEBOOKS
if "%choice%"=="8" goto TEST
if "%choice%"=="9" goto QUICKSTART
if /i "%choice%"=="A" goto HELP

echo.
echo Invalid choice. Please try again.
pause
goto MENU

:FULL_INTERACTIVE
cls
echo Running Full ML Pipeline (Interactive)...
echo.
python main.py --mode full
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:FULL_BATCH
cls
echo Running Full ML Pipeline (Non-Interactive)...
echo.
python main.py --mode full --no-interactive
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:AGENTS_ALL
cls
echo Running Agent Pipeline - All Stages...
echo.
python main.py --mode agents --stage all
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:AGENTS_EDA
cls
echo Running Agent Pipeline - EDA Only...
echo.
python main.py --mode agents --stage eda
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:AGENTS_MODELING
cls
echo Running Agent Pipeline - Modeling Only...
echo.
python main.py --mode agents --stage modeling
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:AGENTS_EXPLAIN
cls
echo Running Agent Pipeline - Explanation Only...
echo.
python main.py --mode agents --stage explain
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:NOTEBOOKS
cls
echo Running Jupyter Notebooks...
echo.
python main.py --mode notebooks
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:TEST
cls
echo Running Quick Test...
echo.
python main.py --mode test
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:QUICKSTART
cls
echo Starting Interactive Python Menu...
echo.
python quickstart.py
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:HELP
cls
python main.py --help
echo.
echo Press any key to return to menu...
pause >nul
goto MENU

:EXIT
echo.
echo Goodbye!
echo.
exit /b 0
