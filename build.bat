@echo off
REM ===================================================================
REM Stickity Stacks - Automated Build Script for Windows
REM This script builds a standalone executable using PyInstaller
REM ===================================================================

echo.
echo ====================================
echo   Stickity Stacks Build Script
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Python found!
echo.

REM Check if PyInstaller is installed, if not install it
echo [2/5] Checking for PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller not found. Installing...
    python -m pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo PyInstaller is ready!
echo.

REM Clean previous builds
echo [3/5] Cleaning previous builds...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist
echo Clean complete!
echo.

REM Build the executable
echo [4/5] Building standalone executable...
echo This may take a few minutes...
pyinstaller build_installer.spec

if %errorlevel% neq 0 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)
echo.

REM Check if executable was created
if not exist "dist\StickityStacks.exe" (
    echo ERROR: Executable was not created!
    pause
    exit /b 1
)

echo [5/5] Build successful!
echo.
echo ====================================
echo   Build Complete!
echo ====================================
echo.
echo Executable location: dist\StickityStacks.exe
echo.
echo You can now:
echo   1. Run the executable directly from dist\StickityStacks.exe
echo   2. Create a desktop shortcut to the executable
echo   3. Build a full installer (see BUILD_INSTALLER.md)
echo.
pause
