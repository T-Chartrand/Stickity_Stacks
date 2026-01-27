# Release Checklist

This guide walks you through creating a new release with pre-built installers.

## 📋 Pre-Release Checklist

Before building and releasing:

- [ ] All changes committed and pushed to `main` branch
- [ ] Version number updated in `installer.iss` (line: `#define MyAppVersion`)
- [ ] CHANGELOG updated with new features/fixes
- [ ] All tests passing
- [ ] README screenshots up to date

## 🔨 Building the Release

### Step 1: Build on Windows

1. **Open Command Prompt** on your Windows machine
2. **Navigate to repository:**
   ```cmd
   cd C:\path\to\Stickity_Stacks
   ```
3. **Run the complete build:**
   ```cmd
   build_complete.bat
   ```
4. **Wait for completion** (2-5 minutes)

### Step 2: Verify Build Outputs

Check that these files exist:

- [ ] `dist\StickityStacks.exe` - Standalone executable (~15 MB)
- [ ] `installer_output\StickityStacks_Setup_v1.0.0.exe` - Full installer (~16 MB)

### Step 3: Test the Installer

**IMPORTANT:** Test before releasing!

1. **Run the installer:**
   ```cmd
   installer_output\StickityStacks_Setup_v1.0.0.exe
   ```

2. **Verify installation:**
   - [ ] Installation completes without errors
   - [ ] App appears in Start Menu
   - [ ] Desktop shortcut created (if selected)
   - [ ] App launches successfully
   - [ ] Can create and save notes
   - [ ] Notes persist after closing and reopening
   - [ ] Settings work (fonts, colors)

3. **Test uninstaller:**
   - [ ] Uninstall from Windows Settings or Control Panel
   - [ ] All files removed (check Program Files)
   - [ ] Start Menu entry removed
   - [ ] Desktop shortcut removed
   - [ ] Optional: Notes file kept/removed as appropriate

## 📦 Creating the GitHub Release

### Option 1: Using GitHub Web Interface (Recommended for First Release)

1. **Go to your repository** on GitHub
2. **Click "Releases"** (right sidebar)
3. **Click "Draft a new release"**

4. **Fill in release details:**
   - **Tag:** `v1.0.0` (create new tag)
   - **Target:** `main` branch
   - **Title:** `Stickity Stacks v1.0.0 - First Official Release`
   - **Description:** See template below

5. **Upload files:**
   - Drag and drop `StickityStacks_Setup_v1.0.0.exe`
   - Optionally upload `StickityStacks.exe` (portable version)

6. **Publish release**

### Option 2: Using GitHub CLI

If you have GitHub CLI installed:

```bash
# Create and upload release
gh release create v1.0.0 \
  installer_output/StickityStacks_Setup_v1.0.0.exe \
  dist/StickityStacks.exe \
  --title "Stickity Stacks v1.0.0 - First Official Release" \
  --notes-file RELEASE_NOTES.md
```

## 📝 Release Description Template

```markdown
# 🎉 Stickity Stacks v1.0.0 - First Official Release

A lightweight, frameless sticky notes application for Windows!

## 🚀 Quick Start

1. **Download** `StickityStacks_Setup_v1.0.0.exe` below
2. **Run** the installer
3. **Launch** from Start Menu
4. **Enjoy** your sticky notes!

No Python installation required! ✨

## 📥 Downloads

### For Most Users
- **StickityStacks_Setup_v1.0.0.exe** (~16 MB)
  - Full installer with uninstaller
  - Start Menu integration
  - Desktop shortcut option
  - **RECOMMENDED**

### For Advanced Users
- **StickityStacks.exe** (~15 MB)
  - Portable version (no installation)
  - Run directly from any folder
  - No uninstaller needed

## ✨ Features

- ✅ Frameless, draggable sticky notes
- ✅ Multiple notes support (Ctrl+N)
- ✅ Resizable windows
- ✅ Custom fonts and colors
- ✅ Auto-save (persistent storage)
- ✅ DPI-aware for high-resolution displays
- ✅ Keyboard shortcuts

## 🎯 System Requirements

- Windows 10 or Windows 11
- 64-bit system
- ~50 MB disk space

## 🐛 Known Issues

- None reported yet!

## 📖 Documentation

- [Quick Start Guide](https://github.com/Hot-snakes/Stickity_Stacks/blob/main/QUICKSTART.md)
- [Windows README](https://github.com/Hot-snakes/Stickity_Stacks/blob/main/README_WINDOWS.md)
- [Full Documentation](https://github.com/Hot-snakes/Stickity_Stacks/blob/main/README.md)

## 🙏 Feedback

Found a bug? Have a feature request? 
[Open an issue](https://github.com/Hot-snakes/Stickity_Stacks/issues)!

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details

---

**Happy note-taking! 📝✨**
```

## 🔄 For Future Releases

### Automated Builds (Coming Soon)

Once GitHub Actions is set up, releases will be automatic:

1. Create and push a version tag:
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

2. GitHub Actions automatically:
   - Builds the executable
   - Creates the installer
   - Uploads to Releases
   - Done! 🎉

## 📊 Post-Release Checklist

After publishing the release:

- [ ] Test download link works
- [ ] Installer downloads correctly
- [ ] Installer runs on a clean Windows machine
- [ ] Update README badge (if using version badge)
- [ ] Announce on social media / forums
- [ ] Monitor issues for bug reports
- [ ] Plan next release features

## 🆘 Troubleshooting

### Build Fails

**Problem:** `build_complete.bat` fails

**Solutions:**
1. Check Python is installed: `python --version`
2. Update PyInstaller: `pip install --upgrade pyinstaller`
3. Run as Administrator
4. Check antivirus isn't blocking

### Installer Build Fails

**Problem:** Inno Setup fails

**Solutions:**
1. Make sure executable exists: `dist\StickityStacks.exe`
2. Check Inno Setup is installed at default location
3. Run Inno Setup manually on `installer.iss`

### File Too Large for GitHub

**Problem:** Installer over 100 MB

**Solutions:**
1. Use GitHub Releases (supports larger files)
2. Optimize with UPX compression (already enabled)
3. Consider hosting on external service

## 📈 Version Numbering

Follow Semantic Versioning (SemVer):

- `v1.0.0` - Major.Minor.Patch
- **Major** (1.x.x): Breaking changes
- **Minor** (x.1.x): New features, backwards compatible
- **Patch** (x.x.1): Bug fixes

Examples:
- `v1.0.0` - First release
- `v1.0.1` - Bug fix
- `v1.1.0` - New feature (e.g., note export)
- `v2.0.0` - Major rewrite or breaking change

## 🎯 Next Steps

After your first release:

1. ⭐ **Get feedback** from users
2. 🐛 **Fix reported bugs**
3. ✨ **Plan new features**
4. 🔄 **Repeat release process**

---

**You've got this! 🚀**

Questions? Open an issue on GitHub!
