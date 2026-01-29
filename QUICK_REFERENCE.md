# Stickity Stacks - Deployment Quick Reference Card

## 🎯 One-Page Command Reference

### Most Common Commands

```cmd
┌─────────────────────────────────────────────────────────────┐
│ BUILD & DEPLOY                                              │
├─────────────────────────────────────────────────────────────┤
│ Full Build:          deployment\deploy_local.bat            │
│ Portable:            deployment\build_portable.bat          │
│ Quick Test:          build.bat                              │
│ Full Build+Install:  build_complete.bat                     │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ VERSION MANAGEMENT                                          │
├─────────────────────────────────────────────────────────────┤
│ Bug Fix:     python deployment\version_bump.py patch        │
│ Feature:     python deployment\version_bump.py minor        │
│ Breaking:    python deployment\version_bump.py major        │
│ Custom:      python deployment\version_bump.py 1.2.3        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ TESTING                                                     │
├─────────────────────────────────────────────────────────────┤
│ Full Test:   pwsh deployment\test_deployment.ps1            │
│ Verbose:     pwsh deployment\test_deployment.ps1 -Verbose   │
│ Skip Install: pwsh deployment\test_deployment.ps1 -SkipInstall│
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ RELEASE WORKFLOW                                            │
├─────────────────────────────────────────────────────────────┤
│ 1. Update version:                                          │
│    python deployment\version_bump.py minor                  │
│                                                             │
│ 2. Edit CHANGELOG.md (fill in changes)                      │
│                                                             │
│ 3. Commit & tag:                                            │
│    git add -A                                               │
│    git commit -m "Release v1.1.0"                           │
│    git tag v1.1.0                                           │
│    git push origin v1.1.0                                   │
│                                                             │
│ 4. GitHub Actions builds and releases automatically! 🎉     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Important File Locations

```
Executable:      dist\StickityStacks.exe
Installer:       installer_output\StickityStacks_Setup_v1.0.0.exe
Portable:        releases\StickityStacks_Portable_v1.0.0.zip
Checksums:       dist\checksums\
Test Results:    deployment_test_results_*.json
```

---

## 🔧 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | `pip install --upgrade pyinstaller` |
| Inno Setup not found | Install from jrsoftware.org/isdl.php |
| Tests fail | Run PowerShell as Administrator |
| GitHub Actions not running | Check Actions tab enabled |
| SmartScreen warning | Normal for unsigned apps |

---

## 📊 Build Status Indicators

### ✅ Success Indicators
- All tests passed (>90%)
- Executable ~15 MB
- Installer ~16 MB
- No error logs
- Clean uninstall

### ⚠️ Warning Indicators
- Some tests failed (70-90%)
- File sizes unusual
- Build warnings
- Slow build time (>10 min)

### ❌ Failure Indicators
- Build errors
- Many tests failed (<70%)
- Missing files
- Crashes during testing

---

## 🎯 Quality Checklist

Before each release:
- [ ] All tests pass (deployment\test_deployment.ps1)
- [ ] Tested on clean Windows 11 VM
- [ ] Version number updated
- [ ] CHANGELOG.md updated
- [ ] No console warnings
- [ ] Installer works silently
- [ ] Uninstaller works
- [ ] Notes persist correctly

---

## 🚀 Distribution Channels

| Channel | Status | Setup Time | Reach |
|---------|--------|------------|-------|
| GitHub Releases | ✅ Ready | 0 min | High |
| Portable ZIP | ✅ Ready | 0 min | Medium |
| Silent Install | ✅ Ready | 0 min | Enterprise |
| Chocolatey | ⏳ Not Set Up | 1-2 hrs | High |
| WinGet | ⏳ Not Set Up | 1-2 hrs | High |
| Microsoft Store | ⏳ Not Set Up | 4-8 hrs | Very High |

---

## 💡 Pro Tips

**Speed up builds:**
```cmd
REM Don't clean build folder
pyinstaller --noconfirm build_installer.spec
```

**Debug issues:**
```python
# In spec file
console=True  # Shows errors
```

**Silent deployment:**
```cmd
StickityStacks_Setup_v1.0.0.exe /VERYSILENT /NORESTART
```

**Verify checksums:**
```powershell
certutil -hashfile dist\StickityStacks.exe SHA256
```

---

## 📞 Support

- 📖 Full Guide: `deployment\DEPLOYMENT_GUIDE.md`
- 📝 Summary: `DEPLOYMENT_SUMMARY.md`
- 🐛 Issues: github.com/Hot-snakes/Stickity_Stacks/issues
- 📧 Email: mr0tstihs81@gmail.com

---

## 🎉 Quick Win

**Deploy your first release right now:**

```cmd
cd D:\Stickity-Stacks
deployment\deploy_local.bat
```

✅ Builds everything
✅ Creates checksums
✅ Ready to distribute

**That's it! You're done! 🚀**

---

*Keep this card handy for quick reference!*
