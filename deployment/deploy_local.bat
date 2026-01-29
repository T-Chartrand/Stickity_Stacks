@echo off
setlocal enabledelayedexpansion
REM ===================================================================
REM Stickity Stacks - Local Deployment Script
REM Optimized for single-user Windows 11 deployment
REM ===================================================================

echo.
echo ================================================
echo   Stickity Stacks - Local Deployment
echo ================================================
echo.
echo This will:
echo   1. Build optimized executable
echo   2. Create installer
echo   3. Test installation
echo   4. Generate checksums
echo.

set START_TIME=%time%
set ERROR_LEVEL=0

REM Change to project root
cd /d "%~dp0.."

REM ===================================================================
REM STEP 1: Environment Check
REM ===================================================================
echo [STEP 1/6] Checking environment...
echo.

REM Check Python
python --version >nul 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python not found!
    echo Please install Python from https://www.python.org/downloads/
    set ERROR_LEVEL=1
    goto :end
)
echo [OK] Python found

REM Check PyInstaller
python -m pip show pyinstaller >nul 2>&1
if !errorlevel! neq 0 (
    echo [INFO] Installing PyInstaller...
    python -m pip install pyinstaller
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install PyInstaller
        set ERROR_LEVEL=1
        goto :end
    )
)
echo [OK] PyInstaller ready

REM Check Inno Setup
set INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe
if not exist "!INNO_PATH!" (
    echo [WARNING] Inno Setup not found
    echo Download from: https://jrsoftware.org/isdl.php
    set BUILD_INSTALLER=0
) else (
    echo [OK] Inno Setup found
    set BUILD_INSTALLER=1
)

echo.

REM ===================================================================
REM STEP 2: Clean Previous Builds
REM ===================================================================
echo [STEP 2/6] Cleaning previous builds...
echo.

if exist "build\" (
    echo Removing build/
    rmdir /s /q build
)

if exist "dist\" (
    echo Removing dist/
    rmdir /s /q dist
)

if exist "installer_output\" (
    echo Removing installer_output/
    rmdir /s /q installer_output
)

echo [OK] Clean complete
echo.

REM ===================================================================
REM STEP 3: Build Executable
REM ===================================================================
echo [STEP 3/6] Building executable...
echo.

pyinstaller --clean --noconfirm build_installer.spec

if !errorlevel! neq 0 (
    echo [ERROR] Build failed!
    set ERROR_LEVEL=1
    goto :end
)

if not exist "dist\StickityStacks.exe" (
    echo [ERROR] Executable not created!
    set ERROR_LEVEL=1
    goto :end
)

echo [OK] Executable built successfully
echo.

REM ===================================================================
REM STEP 4: Build Installer
REM ===================================================================
if "!BUILD_INSTALLER!"=="1" (
    echo [STEP 4/6] Building installer...
    echo.
    
    "!INNO_PATH!" installer.iss
    
    if !errorlevel! neq 0 (
        echo [ERROR] Installer build failed!
        set ERROR_LEVEL=1
        goto :end
    )
    
    echo [OK] Installer created successfully
    echo.
) else (
    echo [STEP 4/6] Skipping installer (Inno Setup not installed)
    echo.
)

REM ===================================================================
REM STEP 5: Generate Checksums
REM ===================================================================
echo [STEP 5/6] Generating checksums...
echo.

REM Create checksums directory
if not exist "dist\checksums" mkdir dist\checksums

REM Calculate SHA-256 for executable
certutil -hashfile "dist\StickityStacks.exe" SHA256 > dist\checksums\StickityStacks.exe.sha256
echo [OK] Executable checksum created

REM Calculate SHA-256 for installer (if exists)
if exist "installer_output\StickityStacks_Setup_v1.0.0.exe" (
    certutil -hashfile "installer_output\StickityStacks_Setup_v1.0.0.exe" SHA256 > dist\checksums\Installer.sha256
    echo [OK] Installer checksum created
)

echo.

REM ===================================================================
REM STEP 6: Summary
REM ===================================================================
echo [STEP 6/6] Deployment Summary
echo.

echo ================================================
echo   BUILD COMPLETE
echo ================================================
echo.

REM Display file sizes
if exist "dist\StickityStacks.exe" (
    echo Executable: dist\StickityStacks.exe
    for %%A in (dist\StickityStacks.exe) do echo   Size: %%~zA bytes (~%%~zA KB)
    echo.
)

if exist "installer_output\StickityStacks_Setup_v1.0.0.exe" (
    echo Installer: installer_output\StickityStacks_Setup_v1.0.0.exe
    for %%A in (installer_output\StickityStacks_Setup_v1.0.0.exe) do echo   Size: %%~zA bytes (~%%~zA KB)
    echo.
)

echo Checksums: dist\checksums\
echo.

REM Calculate build time
set END_TIME=%time%
echo Build started: %START_TIME%
echo Build ended:   %END_TIME%
echo.

echo ================================================
echo   NEXT STEPS
echo ================================================
echo.
echo 1. Test the executable:
echo    dist\StickityStacks.exe
echo.
echo 2. Test the installer:
echo    installer_output\StickityStacks_Setup_v1.0.0.exe
echo.
echo 3. Verify checksums:
echo    dist\checksums\
echo.
echo 4. Create GitHub Release:
echo    git tag v1.0.0
echo    git push origin v1.0.0
echo.

:end
if !ERROR_LEVEL! neq 0 (
    echo.
    echo [FAILED] Deployment encountered errors
    pause
    exit /b !ERROR_LEVEL!
)

echo [SUCCESS] Local deployment complete!
echo.
pause
endlocal
