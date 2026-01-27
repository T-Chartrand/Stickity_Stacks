@echo off
setlocal enabledelayedexpansion
REM ===================================================================
REM Stickity Stacks - Complete Installer Build Script
REM This script builds BOTH the executable AND the installer
REM ===================================================================

echo.
echo ===============================================
echo   Stickity Stacks Complete Installer Builder
echo ===============================================
echo.
echo This will:
echo   1. Build standalone executable
echo   2. Create Windows installer
echo.

REM Check Python
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check Inno Setup - using delayed expansion and proper escaping
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "!INNO_PATH!" (
    echo.
    echo WARNING: Inno Setup not found at:
    echo !INNO_PATH!
    echo.
    echo You can:
    echo   1. Install Inno Setup from https://jrsoftware.org/isdl.php
    echo   2. Or just build the executable without installer
    echo.
    set /p choice="Build executable only? (Y/N): "
    if /i "!choice!" neq "Y" (
        echo Build cancelled.
        pause
        exit /b 1
    )
    set BUILD_EXE_ONLY=1
) else (
    echo [OK] Inno Setup found
    set BUILD_EXE_ONLY=0
)
echo.

REM Install PyInstaller
echo Checking PyInstaller...
pip show pyinstaller >nul 2>&1
if !errorlevel! neq 0 (
    echo Installing PyInstaller...
    pip install pyinstaller
    if !errorlevel! neq 0 (
        echo ERROR: Failed to install PyInstaller
        pause
        exit /b 1
    )
)
echo [OK] PyInstaller ready
echo.

REM Clean old builds
echo Cleaning old builds...
if exist "build\" rmdir /s /q build
if exist "dist\" rmdir /s /q dist
if exist "installer_output\" rmdir /s /q installer_output
echo [OK] Clean complete
echo.

REM Build executable
echo ===============================================
echo   STEP 1: Building Executable
echo ===============================================
echo.
pyinstaller build_installer.spec

if !errorlevel! neq 0 (
    echo.
    echo ERROR: Executable build failed!
    pause
    exit /b 1
)

if not exist "dist\StickityStacks.exe" (
    echo.
    echo ERROR: Executable not created!
    pause
    exit /b 1
)

echo.
echo [OK] Executable built successfully!
echo      Location: dist\StickityStacks.exe
echo.

REM Build installer if Inno Setup is available
if "!BUILD_EXE_ONLY!"=="1" (
    echo.
    echo ===============================================
    echo   Build Complete (Executable Only)
    echo ===============================================
    echo.
    echo Your executable is ready at:
    echo   dist\StickityStacks.exe
    echo.
    echo To create an installer:
    echo   1. Install Inno Setup from https://jrsoftware.org/isdl.php
    echo   2. Run this script again
    echo.
    pause
    exit /b 0
)

echo ===============================================
echo   STEP 2: Building Installer
echo ===============================================
echo.

"!INNO_PATH!" installer.iss

if !errorlevel! neq 0 (
    echo.
    echo ERROR: Installer build failed!
    echo.
    echo Your executable is still available at:
    echo   dist\StickityStacks.exe
    echo.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo   BUILD COMPLETE!
echo ===============================================
echo.
echo Executable:  dist\StickityStacks.exe
echo Installer:   installer_output\StickityStacks_Setup_v1.0.0.exe
echo.
echo You can now:
echo   1. Test the executable: dist\StickityStacks.exe
echo   2. Distribute the installer to users
echo   3. Upload to GitHub Releases
echo.
echo File sizes:
dir /s dist\StickityStacks.exe | find "StickityStacks.exe"
dir /s installer_output\*.exe | find ".exe"
echo.
pause
endlocal
