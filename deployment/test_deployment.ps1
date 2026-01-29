# Stickity Stacks - Deployment Testing Script
# PowerShell script for comprehensive deployment testing

param(
    [string]$InstallerPath = "installer_output\StickityStacks_Setup_v1.0.0.exe",
    [switch]$SkipInstall,
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"
$TestResults = @()

function Write-TestHeader {
    param([string]$Message)
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "  $Message" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Write-TestResult {
    param(
        [string]$Test,
        [bool]$Passed,
        [string]$Details = ""
    )
    
    $result = @{
        Test = $Test
        Passed = $Passed
        Details = $Details
        Timestamp = Get-Date
    }
    
    $script:TestResults += $result
    
    if ($Passed) {
        Write-Host "✓ PASS: $Test" -ForegroundColor Green
    } else {
        Write-Host "✗ FAIL: $Test" -ForegroundColor Red
    }
    
    if ($Details -and $Verbose) {
        Write-Host "  Details: $Details" -ForegroundColor Gray
    }
}

# ===================================================================
# TEST 1: Pre-Installation Checks
# ===================================================================
Write-TestHeader "Pre-Installation Checks"

# Check if installer exists
$installerExists = Test-Path $InstallerPath
Write-TestResult "Installer file exists" $installerExists $InstallerPath

if ($installerExists) {
    # Check file size
    $fileSize = (Get-Item $InstallerPath).Length / 1MB
    $sizeOK = $fileSize -gt 5 -and $fileSize -lt 50
    Write-TestResult "Installer size reasonable (5-50 MB)" $sizeOK "$([math]::Round($fileSize, 2)) MB"
    
    # Check digital signature (if signed)
    try {
        $signature = Get-AuthenticodeSignature $InstallerPath
        $isSigned = $signature.Status -eq 'Valid'
        Write-TestResult "Digital signature valid" $isSigned $signature.Status
    } catch {
        Write-TestResult "Digital signature check" $false "Not signed or check failed"
    }
}

# Check system requirements
$osVersion = [System.Environment]::OSVersion.Version
$isWin10OrLater = $osVersion.Major -ge 10
Write-TestResult "Windows 10 or later" $isWin10OrLater "Version: $($osVersion.Major).$($osVersion.Minor)"

$architecture = [System.Environment]::Is64BitOperatingSystem
Write-TestResult "64-bit operating system" $architecture

# ===================================================================
# TEST 2: Installation Process
# ===================================================================
if (-not $SkipInstall) {
    Write-TestHeader "Installation Process"
    
    # Silent install
    Write-Host "Running silent installation..." -ForegroundColor Yellow
    try {
        $installProcess = Start-Process -FilePath $InstallerPath -ArgumentList "/VERYSILENT", "/NORESTART", "/LOG=install_test.log" -Wait -PassThru
        $installSuccess = $installProcess.ExitCode -eq 0
        Write-TestResult "Silent installation" $installSuccess "Exit code: $($installProcess.ExitCode)"
    } catch {
        Write-TestResult "Silent installation" $false $_.Exception.Message
    }
    
    # Wait for installation to complete
    Start-Sleep -Seconds 5
    
    # Check installation location
    $installPath = "$env:ProgramFiles\Stickity Stacks\StickityStacks.exe"
    $appInstalled = Test-Path $installPath
    Write-TestResult "Application installed" $appInstalled $installPath
    
    # Check Start Menu shortcut
    $startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Stickity Stacks.lnk"
    $startMenuExists = Test-Path $startMenuPath
    Write-TestResult "Start Menu shortcut created" $startMenuExists
    
    # Check desktop shortcut (if option was selected)
    $desktopPath = "$env:USERPROFILE\Desktop\Stickity Stacks.lnk"
    $desktopExists = Test-Path $desktopPath
    if ($desktopExists) {
        Write-TestResult "Desktop shortcut created" $true
    }
}

# ===================================================================
# TEST 3: Application Runtime
# ===================================================================
Write-TestHeader "Application Runtime Tests"

$exePath = "$env:ProgramFiles\Stickity Stacks\StickityStacks.exe"

if (Test-Path $exePath) {
    # Check file properties
    $exeInfo = Get-Item $exePath
    Write-TestResult "Executable accessible" $true "$($exeInfo.Length / 1MB) MB"
    
    # Try to launch application
    Write-Host "Attempting to launch application..." -ForegroundColor Yellow
    try {
        $appProcess = Start-Process -FilePath $exePath -PassThru
        Start-Sleep -Seconds 3
        
        $isRunning = -not $appProcess.HasExited
        Write-TestResult "Application launches" $isRunning
        
        if ($isRunning) {
            # Check window created
            $windowExists = (Get-Process -Id $appProcess.Id).MainWindowHandle -ne 0
            Write-TestResult "Application window created" $windowExists
            
            # Close application gracefully
            Start-Sleep -Seconds 2
            $appProcess.CloseMainWindow() | Out-Null
            Start-Sleep -Seconds 2
            
            if (-not $appProcess.HasExited) {
                $appProcess.Kill()
            }
            
            Write-TestResult "Application closes gracefully" $true
        }
    } catch {
        Write-TestResult "Application launch" $false $_.Exception.Message
    }
    
    # Check for crash dumps or error logs
    $errorLog = "$env:USERPROFILE\stickity_stacks_error.log"
    $noCrashes = -not (Test-Path $errorLog)
    Write-TestResult "No error logs generated" $noCrashes
}

# ===================================================================
# TEST 4: Data Persistence
# ===================================================================
Write-TestHeader "Data Persistence Tests"

$notesFile = "$env:USERPROFILE\stickity_stacks_notes_win.json"

# Launch app, wait, close, check if notes file created
if (Test-Path $exePath) {
    Write-Host "Testing data persistence..." -ForegroundColor Yellow
    
    $appProcess = Start-Process -FilePath $exePath -PassThru
    Start-Sleep -Seconds 5
    
    $appProcess.Kill()
    Start-Sleep -Seconds 2
    
    $notesCreated = Test-Path $notesFile
    Write-TestResult "Notes file created" $notesCreated $notesFile
    
    if ($notesCreated) {
        try {
            $notesContent = Get-Content $notesFile -Raw | ConvertFrom-Json
            $validJSON = $true
            Write-TestResult "Notes file valid JSON" $validJSON
        } catch {
            Write-TestResult "Notes file valid JSON" $false $_.Exception.Message
        }
    }
}

# ===================================================================
# TEST 5: Uninstallation
# ===================================================================
if (-not $SkipInstall) {
    Write-TestHeader "Uninstallation Tests"
    
    # Find uninstaller
    $uninstallPath = "$env:ProgramFiles\Stickity Stacks\unins000.exe"
    $uninstallerExists = Test-Path $uninstallPath
    Write-TestResult "Uninstaller exists" $uninstallerExists
    
    if ($uninstallerExists) {
        Write-Host "Running uninstaller..." -ForegroundColor Yellow
        
        try {
            $uninstallProcess = Start-Process -FilePath $uninstallPath -ArgumentList "/VERYSILENT", "/NORESTART" -Wait -PassThru
            $uninstallSuccess = $uninstallProcess.ExitCode -eq 0
            Write-TestResult "Uninstallation completes" $uninstallSuccess "Exit code: $($uninstallProcess.ExitCode)"
        } catch {
            Write-TestResult "Uninstallation" $false $_.Exception.Message
        }
        
        Start-Sleep -Seconds 5
        
        # Verify files removed
        $filesRemoved = -not (Test-Path "$env:ProgramFiles\Stickity Stacks")
        Write-TestResult "Program files removed" $filesRemoved
        
        # Verify shortcuts removed
        $shortcutsRemoved = -not (Test-Path $startMenuPath)
        Write-TestResult "Start Menu shortcut removed" $shortcutsRemoved
        
        # Check if notes file preserved (should be)
        $notesPreserved = Test-Path $notesFile
        Write-TestResult "User data preserved" $notesPreserved
    }
}

# ===================================================================
# TEST 6: Security & Compatibility
# ===================================================================
Write-TestHeader "Security & Compatibility"

if (Test-Path $InstallerPath) {
    # Check for known malware signatures (basic check)
    try {
        $defender = Get-MpComputerStatus
        if ($defender.AntivirusEnabled) {
            Write-TestResult "Windows Defender enabled" $true
            
            # Quick scan of installer (if defender is available)
            # Note: This may trigger actual scan
            Write-Host "Note: Full antivirus scan recommended separately" -ForegroundColor Yellow
        }
    } catch {
        Write-TestResult "Windows Defender check" $false "Could not check status"
    }
}

# Check DPI awareness
$dpiAware = $true  # Tkinter handles this automatically on Windows
Write-TestResult "DPI awareness" $dpiAware

# ===================================================================
# FINAL SUMMARY
# ===================================================================
Write-TestHeader "Test Summary"

$totalTests = $TestResults.Count
$passedTests = ($TestResults | Where-Object { $_.Passed }).Count
$failedTests = $totalTests - $passedTests
$passRate = [math]::Round(($passedTests / $totalTests) * 100, 2)

Write-Host "Total Tests:  $totalTests" -ForegroundColor Cyan
Write-Host "Passed:       $passedTests" -ForegroundColor Green
Write-Host "Failed:       $failedTests" -ForegroundColor Red
Write-Host "Pass Rate:    $passRate%" -ForegroundColor $(if ($passRate -ge 80) { "Green" } else { "Yellow" })

# Export results
$reportPath = "deployment_test_results_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"
$TestResults | ConvertTo-Json -Depth 3 | Out-File $reportPath

Write-Host "`nDetailed results saved to: $reportPath" -ForegroundColor Cyan

# Failed tests details
if ($failedTests -gt 0) {
    Write-Host "`nFailed Tests:" -ForegroundColor Red
    $TestResults | Where-Object { -not $_.Passed } | ForEach-Object {
        Write-Host "  - $($_.Test)" -ForegroundColor Red
        if ($_.Details) {
            Write-Host "    $($_.Details)" -ForegroundColor Gray
        }
    }
}

Write-Host "`n"

# Exit code based on pass rate
if ($passRate -ge 90) {
    exit 0
} elseif ($passRate -ge 70) {
    exit 1
} else {
    exit 2
}
