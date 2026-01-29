@echo off
setlocal enabledelayedexpansion
REM ===================================================================
REM Stickity Stacks - Portable Version Builder
REM Creates a ZIP package with standalone executable
REM ===================================================================

echo.
echo ================================================
echo   Stickity Stacks - Portable Builder
echo ================================================
echo.

cd /d "%~dp0.."

REM Version from installer.iss (we'll extract it)
set VERSION=1.0.0

REM ===================================================================
REM Build Executable First
REM ===================================================================
echo [1/4] Building executable...
echo.

if not exist "dist\StickityStacks.exe" (
    echo Executable not found. Building...
    call build.bat
    if !errorlevel! neq 0 (
        echo Build failed!
        pause
        exit /b 1
    )
)

echo [OK] Executable ready
echo.

REM ===================================================================
REM Create Portable Directory Structure
REM ===================================================================
echo [2/4] Creating portable structure...
echo.

set PORTABLE_DIR=portable\StickityStacks_v%VERSION%

if exist "portable\" rmdir /s /q portable
mkdir "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%\docs"

REM Copy executable
copy "dist\StickityStacks.exe" "%PORTABLE_DIR%\"
echo [OK] Copied executable

REM Copy documentation
copy "README_WINDOWS.md" "%PORTABLE_DIR%\docs\README.txt"
copy "LICENSE" "%PORTABLE_DIR%\docs\"
echo [OK] Copied documentation

REM Create portable README
echo Creating portable README...
(
echo ================================================
echo   Stickity Stacks - Portable Edition
echo ================================================
echo.
echo Version: %VERSION%
echo.
echo QUICK START:
echo   1. Double-click StickityStacks.exe to run
echo   2. No installation required!
echo.
echo FEATURES:
echo   - Runs from any location
echo   - USB drive compatible
echo   - No registry modifications
echo   - Notes saved in same directory
echo.
echo KEYBOARD SHORTCUTS:
echo   Ctrl+N - New note
echo   Ctrl+D - Delete note
echo.
echo DATA LOCATION:
echo   Notes are saved to:
echo   %USERPROFILE%\stickity_stacks_notes_win.json
echo.
echo   To make truly portable, you can move this file
echo   to the same directory as the executable.
echo.
echo DOCUMENTATION:
echo   See docs\ folder for full documentation
echo.
echo SUPPORT:
echo   GitHub: https://github.com/Hot-snakes/Stickity_Stacks
echo   Issues: https://github.com/Hot-snakes/Stickity_Stacks/issues
echo.
echo ================================================
) > "%PORTABLE_DIR%\README_PORTABLE.txt"

echo [OK] Created portable README
echo.

REM ===================================================================
REM Create ZIP Archive
REM ===================================================================
echo [3/4] Creating ZIP archive...
echo.

if not exist "releases\" mkdir releases

set ZIP_NAME=releases\StickityStacks_Portable_v%VERSION%.zip

REM Use PowerShell to create ZIP
powershell -Command "Compress-Archive -Path '%PORTABLE_DIR%\*' -DestinationPath '%ZIP_NAME%' -Force"

if !errorlevel! neq 0 (
    echo [ERROR] Failed to create ZIP archive
    pause
    exit /b 1
)

echo [OK] ZIP archive created
echo.

REM ===================================================================
REM Generate Checksum
REM ===================================================================
echo [4/4] Generating checksum...
echo.

certutil -hashfile "%ZIP_NAME%" SHA256 > "%ZIP_NAME%.sha256"

echo [OK] Checksum created
echo.

REM ===================================================================
REM Summary
REM ===================================================================
echo ================================================
echo   PORTABLE BUILD COMPLETE
echo ================================================
echo.
echo Portable package: %ZIP_NAME%
for %%A in ("%ZIP_NAME%") do echo   Size: %%~zA bytes
echo.
echo Checksum: %ZIP_NAME%.sha256
echo.
echo Contents:
echo   - StickityStacks.exe
echo   - README_PORTABLE.txt
echo   - docs\README.txt
echo   - docs\LICENSE
echo.
echo You can now distribute this ZIP file!
echo Users can extract and run without installation.
echo.

pause
endlocal
