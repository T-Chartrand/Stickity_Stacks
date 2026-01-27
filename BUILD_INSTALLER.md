# Building a Standalone Installer for Windows

This guide will help you create a professional Windows installer for Stickity Stacks that can be distributed to end users.

## 🎯 For End Users (Level 1)

If you just want to **use** Stickity Stacks without building it yourself:

1. Download the latest installer from the [Releases](https://github.com/Hot-snakes/Stickity_Stacks/releases) page
2. Double-click `StickityStacks_Setup_v1.0.0.exe`
3. Follow the installation wizard
4. Launch from your Start Menu or Desktop shortcut!

---

## 🔨 For Developers: Building the Installer

### Method 1: Quick Build (Recommended for Testing)

This method creates a standalone executable without a full installer.

#### Prerequisites
- Python 3.6 or higher installed
- Internet connection (for downloading PyInstaller)

#### Steps

1. **Clone the repository:**
   ```cmd
   git clone https://github.com/Hot-snakes/Stickity_Stacks.git
   cd Stickity_Stacks
   ```

2. **Run the automated build script:**
   ```cmd
   build.bat
   ```

3. **Find your executable:**
   - Location: `dist\StickityStacks.exe`
   - You can now run this file directly or share it with others!

**What the script does:**
- ✅ Checks for Python installation
- ✅ Installs PyInstaller if needed
- ✅ Cleans old build files
- ✅ Builds a standalone executable
- ✅ Reports success/failure

---

### Method 2: Full Installer (Recommended for Distribution)

This method creates a professional Windows installer (`.exe`) that includes:
- Automated installation wizard
- Start Menu shortcuts
- Desktop shortcut option
- Proper uninstaller
- License agreement display

#### Prerequisites

1. **Python 3.6+** - [Download here](https://www.python.org/downloads/)
2. **Inno Setup 6+** - [Download here](https://jrsoftware.org/isdl.php)

#### Steps

1. **Build the standalone executable first:**
   ```cmd
   build.bat
   ```

2. **Install Inno Setup:**
   - Download and install Inno Setup from the link above
   - Use default installation settings

3. **Build the installer:**
   - Right-click `installer.iss` 
   - Select "Compile" (or open in Inno Setup and click "Compile")
   
   **OR** from command line:
   ```cmd
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
   ```

4. **Find your installer:**
   - Location: `installer_output\StickityStacks_Setup_v1.0.0.exe`
   - This is a complete installer ready for distribution!

---

## 📦 Installer Features

The generated installer includes:

✅ **User-Friendly Installation**
- Modern wizard-style interface
- Customizable installation directory
- Optional desktop shortcut
- Optional Quick Launch icon

✅ **Smart Uninstallation**
- Removes all program files
- Option to keep user notes
- Clean registry cleanup

✅ **Professional Polish**
- Application icon
- License agreement display
- Start Menu integration
- Proper Windows integration

---

## 🔧 Advanced Configuration

### Customizing the Build

Edit `build_installer.spec` to customize:
```python
# Change app name
name='StickityStacks'

# Include additional files
datas=[('myfile.txt', '.')],

# Hide console window (default: False)
console=False
```

### Customizing the Installer

Edit `installer.iss` to customize:
```ini
; App version
#define MyAppVersion "1.0.0"

; Installation directory
DefaultDirName={autopf}\{#MyAppName}

; Require admin privileges
PrivilegesRequired=admin

; Include additional files
Source: "myfile.txt"; DestDir: "{app}"; Flags: ignoreversion
```

---

## 📝 Build Checklist

Before distributing your installer:

- [ ] Test on a clean Windows machine
- [ ] Verify all shortcuts work
- [ ] Check that notes persist after restart
- [ ] Test uninstaller completely removes the app
- [ ] Scan with antivirus software
- [ ] Test on both Windows 10 and 11
- [ ] Verify DPI scaling on high-resolution displays

---

## 🐛 Troubleshooting

### Build Script Fails

**"Python is not installed or not in PATH"**
- Solution: Install Python and check "Add Python to PATH" during installation
- Verify: Run `python --version` in Command Prompt

**"PyInstaller installation failed"**
- Solution: Run `pip install --upgrade pip` then try again
- Alternative: Manually install with `pip install pyinstaller`

**"Build failed" error**
- Check that all files are present (especially `stickity_stacks_win.py`)
- Ensure no antivirus is blocking PyInstaller
- Try running Command Prompt as Administrator

### Inno Setup Fails

**"Cannot find file"**
- Make sure you ran `build.bat` first
- Verify `dist\StickityStacks.exe` exists
- Check that `LICENSE` file exists

**"Permission denied"**
- Run Inno Setup Compiler as Administrator
- Close any running instances of the app

### Runtime Issues

**Executable won't start**
- Make sure all dependencies are included in the spec file
- Check Windows Event Viewer for error details
- Try building with `console=True` to see error messages

**Notes don't save**
- Check write permissions in `%USERPROFILE%`
- Run executable as Administrator (one time) to verify

---

## 📤 Distribution Options

Once you have your installer:

### Option 1: GitHub Releases
1. Go to your repository → Releases → Create new release
2. Upload `StickityStacks_Setup_v1.0.0.exe`
3. Add release notes
4. Publish!

### Option 2: Personal Website
- Host the installer on your website
- Provide SHA-256 checksum for verification
- Include installation instructions

### Option 3: Microsoft Store
- Package as MSIX (advanced)
- Submit to Microsoft Store
- Reach wider audience

---

## 🔒 Code Signing (Optional but Recommended)

For production releases, consider code signing your installer to:
- Eliminate Windows SmartScreen warnings
- Build user trust
- Verify authenticity

**Options:**
- Purchase certificate from DigiCert, Sectigo, etc.
- Use free code signing for open-source projects
- Sign with `signtool` (included with Windows SDK)

**Example:**
```cmd
signtool sign /f mycert.pfx /p password StickityStacks_Setup_v1.0.0.exe
```

---

## 📊 File Size Comparison

| Build Type | Size | Pros | Cons |
|------------|------|------|------|
| Python Script | ~10 KB | Smallest | Requires Python |
| Standalone EXE | ~15 MB | No dependencies | Larger file |
| Installer | ~16 MB | Professional | Slightly larger |

---

## 🎓 Next Steps

- **For Users:** Download from Releases and enjoy!
- **For Developers:** Customize the app and rebuild
- **For Contributors:** Submit pull requests with improvements!

---

## 💡 Tips for Level 1 Users

**First time building software?**
1. Don't panic! Follow the steps carefully
2. Read error messages - they usually tell you what's wrong
3. Google any error messages you don't understand
4. Join our community for help (link in main README)

**Need help?**
- Open an issue on GitHub
- Check existing issues for solutions
- Contact the maintainer

---

## 📋 Quick Reference

```cmd
# Build standalone executable
build.bat

# Build installer (after executable is built)
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss

# Manual PyInstaller build
pip install pyinstaller
pyinstaller build_installer.spec

# Test the executable
dist\StickityStacks.exe
```

---

**Happy Building! 🎉**

For questions, issues, or suggestions, please visit our [GitHub Issues](https://github.com/Hot-snakes/Stickity_Stacks/issues) page.
