# Stickity Stacks - Windows Installation Guide

## Quick Start for Windows 10/11

### Prerequisites
- Python 3.6 or higher (includes tkinter)
- Windows 10 or Windows 11

### Installation

1. **Verify Python Installation**
   ```cmd
   python --version
   ```

2. **Download the Application**
   - Clone repository: `git clone https://github.com/Hot-snakes/Stickity_Stacks.git`
   - Or download ZIP and extract

3. **Run the Application**
   ```cmd
   cd Stickity_Stacks
   python stickity_stacks_win.py
   ```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | Create new note |
| `Ctrl+S` | Create new note (alternative) |
| `Ctrl+D` | Delete current note |

### Features

- ✅ Frameless, draggable sticky notes
- ✅ Resizable windows (drag bottom-right corner)
- ✅ Custom fonts and colors
- ✅ Persistent storage (auto-save)
- ✅ Multiple notes support
- ✅ DPI awareness for high-resolution displays

### Creating Desktop Shortcut

1. Right-click `stickity_stacks_win.py`
2. Select "Create shortcut"
3. Move shortcut to Desktop
4. Right-click shortcut → Properties → Change icon (optional)

### Troubleshooting

**"Python not found"**
- Install Python from https://www.python.org/downloads/
- During installation, check "Add Python to PATH"

**Application won't start**
- Open Command Prompt and run: `python stickity_stacks_win.py`
- Check error messages for specific issues

**Notes not saving**
- Check write permissions in home directory
- Location: `C:\Users\YourName\stickity_stacks_notes_win.json`

### Data Storage

Notes are automatically saved to:
```
%USERPROFILE%\stickity_stacks_notes_win.json
```

### Uninstallation

1. Delete application folder
2. Delete notes file: `%USERPROFILE%\stickity_stacks_notes_win.json`

---

**Platform**: Windows 10/11
**Language**: Python 3.6+
**GUI Framework**: tkinter (built-in)
