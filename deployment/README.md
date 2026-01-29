# Deployment Tools

This directory contains all the automation tools for building, testing, and deploying Stickity Stacks on Windows 11.

## 📚 Documentation

Start here:
1. **[QUICK_REFERENCE.md](../QUICK_REFERENCE.md)** - One-page command reference
2. **[DEPLOYMENT_SUMMARY.md](../DEPLOYMENT_SUMMARY.md)** - What was set up and how to use it
3. **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Comprehensive 70+ page guide
4. **[SETUP_COMPLETE.md](SETUP_COMPLETE.md)** - Detailed setup overview

## 🔧 Scripts

### Build Scripts
- **`deploy_local.bat`** - Complete automated build (recommended)
- **`build_portable.bat`** - Create portable ZIP package

### Utilities
- **`version_bump.py`** - Automated version management
- **`test_deployment.ps1`** - Comprehensive testing suite
- **`create_icon.py`** - PNG to ICO converter

## 🚀 Quick Start

### Build Everything
```cmd
deploy_local.bat
```

### Create Release
```bash
# 1. Update version
python version_bump.py minor

# 2. Commit and tag
git add -A
git commit -m "Release v1.1.0"
git tag v1.1.0
git push origin v1.1.0

# GitHub Actions handles the rest!
```

### Test Deployment
```powershell
powershell -File test_deployment.ps1 -Verbose
```

## 📦 What Gets Built

| File | Description | Size |
|------|-------------|------|
| `dist\StickityStacks.exe` | Standalone executable | ~15 MB |
| `installer_output\StickityStacks_Setup_v1.0.0.exe` | Windows installer | ~16 MB |
| `releases\StickityStacks_Portable_v1.0.0.zip` | Portable package | ~15 MB |
| `dist\checksums\*.sha256` | SHA-256 checksums | <1 KB |

## 🧪 Testing

The test suite validates 25 different aspects:
- Pre-installation checks (6 tests)
- Installation process (4 tests)
- Application runtime (5 tests)
- Data persistence (2 tests)
- Uninstallation (5 tests)
- Security & compatibility (3 tests)

## 📋 Prerequisites

- Python 3.6+ with pip
- PyInstaller (`pip install pyinstaller`)
- Inno Setup 6+ (download from jrsoftware.org)
- Git (for version management)
- PowerShell 5.0+ (for testing)

## 🎯 Common Tasks

### Update Version
```cmd
python version_bump.py patch  # 1.0.0 → 1.0.1
python version_bump.py minor  # 1.0.0 → 1.1.0
python version_bump.py major  # 1.0.0 → 2.0.0
```

### Create Icon
```cmd
pip install Pillow
python create_icon.py
```

### Run Tests
```powershell
# Full test
powershell -ExecutionPolicy Bypass -File test_deployment.ps1

# Verbose output
powershell -File test_deployment.ps1 -Verbose

# Skip installation
powershell -File test_deployment.ps1 -SkipInstall
```

## 🔄 Workflow

```
┌─────────────────┐
│ Update Version  │
│ version_bump.py │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Local Build    │
│ deploy_local.bat│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Test Deploy   │
│test_deployment.ps1│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Commit & Tag   │
│   git push      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ GitHub Actions  │
│  Auto-Release   │
└─────────────────┘
```

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| PyInstaller not found | `pip install pyinstaller` |
| Inno Setup not found | Install from jrsoftware.org |
| Tests fail | Run PowerShell as admin |
| Build errors | Check console output |

## 📞 Support

- Full documentation: See DEPLOYMENT_GUIDE.md
- GitHub Issues: github.com/Hot-snakes/Stickity_Stacks/issues
- Email: mr0tstihs81@gmail.com

## 📄 License

See main repository LICENSE file.

---

**Ready to deploy? Start with:**
```cmd
deploy_local.bat
```
