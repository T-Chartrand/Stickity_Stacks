# Stickity Stacks

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![GTK](https://img.shields.io/badge/GTK-4-green)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey)

A frameless, lightweight sticky note application written in Python. Create, stack, and customize multiple sticky notes with persistent storage and seamless desktop integration.

<div align="center">
  <img src="stickity_stacks.png" alt="Stickity Stacks Icon" width="128">
</div>

## 🚀 Quick Start

### Windows Users
👉 **[Download the installer](https://github.com/Hot-snakes/Stickity_Stacks/releases)** and get started in seconds!

📖 First time? Check out the **[Quick Start Guide](QUICKSTART.md)** for step-by-step instructions.

### Linux Users
See the [Linux installation instructions](#-installation-linux) below.

---

## 📸 Screenshots

<table>
  <tr>
    <td align="center">
      <img src="screenshots/basic-note.png" alt="Basic Note" width="300"><br>
      <em>Clean, frameless sticky note</em>
    </td>
    <td align="center">
      <img src="screenshots/stacked-notes.png" alt="Stacked Notes" width="300"><br>
      <em>Multiple notes with dog-ear indicator</em>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/customization.png" alt="Customization" width="300"><br>
      <em>Different colors and content</em>
    </td>
    <td align="center">
      <img src="screenshots/settings.png" alt="Settings Panel" width="300"><br>
      <em>Font and color customization</em>
    </td>
  </tr>
</table>

## ✨ Features

- **Frameless Design**: Clean, borderless sticky notes that blend seamlessly with your desktop
- **Cross-Platform**: Runs on both Windows (tkinter) and Linux (GTK4)
- **Note Stacking**: Create and manage multiple notes with `Ctrl+S` (Linux) or `Ctrl+N` (Windows)
- **Visual Navigation**: Dog-ear indicator shows current note position in stack (e.g., "2/4") (Linux only)
- **Quick Actions**: Delete notes with `Ctrl+D` or the trash icon
- **Full Customization**: Personalize fonts, text colors, and background colors
- **Drag to Move**: Click and drag anywhere on the note to reposition
- **Resizable Notes**: Drag the bottom-right corner to resize (Windows)
- **Persistent Storage**: All notes and styling preferences are automatically saved
- **Desktop Integration**: Add to your application menu and launcher

---

## 🪟 Windows Installation

### For End Users (Easiest)

1. **Download the installer** from [Releases](https://github.com/Hot-snakes/Stickity_Stacks/releases)
2. Run `StickityStacks_Setup_v1.0.0.exe`
3. Follow the installation wizard
4. Launch from Start Menu!

📖 **Need help?** See the [Quick Start Guide](QUICKSTART.md)

### For Developers

Want to build the installer yourself?

1. **Quick build** (executable only):
   ```cmd
   build.bat
   ```

2. **Complete build** (executable + installer):
   ```cmd
   build_complete.bat
   ```

📖 **Detailed instructions:** [BUILD_INSTALLER.md](BUILD_INSTALLER.md)

### Manual Windows Setup

Don't want to use the installer?

1. Install Python 3.6+ from [python.org](https://www.python.org/downloads/)
2. Clone this repository
3. Run:
   ```cmd
   python stickity_stacks_win.py
   ```

📖 **More details:** [README_WINDOWS.md](README_WINDOWS.md)

---

## 🐧 Installation (Linux)

### Prerequisites

Before installing Stickity Stacks, ensure you have the following dependencies:

- Python 3.6 or higher
- GTK4 development libraries
- Python GObject introspection bindings

### Installing Dependencies

**Fedora/RHEL/CentOS:**
```bash
sudo dnf install python3-gobject gtk4
```

**Ubuntu/Debian:**
```bash
sudo apt install python3-gi gir1.2-gtk-4.0
```

**Arch Linux:**
```bash
sudo pacman -S python-gobject gtk4
```

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Hot-snakes/Stickity_Stacks.git
   cd Stickity_Stacks
   ```

2. **Make the script executable (optional):**
   ```bash
   chmod +x stickity_stacks.py
   ```

3. **Run the application:**
   ```bash
   python3 stickity_stacks.py
   # OR
   ./stickity_stacks.py
   ```

---

## 🎯 Usage

### Keyboard Shortcuts

| Platform | New Note | Delete Note |
|----------|----------|-------------|
| **Linux** | `Ctrl+S` | `Ctrl+D` |
| **Windows** | `Ctrl+N` or `Ctrl+S` | `Ctrl+D` |

### Mouse Controls

- **Move note**: Click and drag anywhere on the note
- **Resize (Windows)**: Drag the bottom-right corner
- **Switch notes (Linux)**: Click the dog-ear corner indicator (shows current position like "2/4")
- **Settings**: Click the gear icon (⚙️) to customize fonts and colors
- **Delete**: Click the trash icon (🗑️) to delete current note

---

## 🖥️ Desktop Integration (Linux)

Add Stickity Stacks to your application menu for easy access:

1. **Copy the desktop file:**
   ```bash
   cp com.stickity.stacks.desktop ~/.local/share/applications/
   ```

2. **Install the application icon:**
   ```bash
   mkdir -p ~/.local/share/icons
   cp stickity_stacks.png ~/.local/share/icons/
   ```

3. **Update the desktop file path (if needed):**
   
   Edit `~/.local/share/applications/com.stickity.stacks.desktop` and ensure the `Exec=` line points to your script:
   ```desktop
   Exec=/full/path/to/stickity_stacks.py
   ```

4. **Refresh the application database:**
   ```bash
   update-desktop-database ~/.local/share/applications
   ```

---

## 🎨 Customization

Stickity Stacks offers extensive customization options:

- **Fonts**: Choose from any system font with size adjustment
- **Text Color**: Pick any color for your note text
- **Background Color**: Customize note background colors
- **Persistent Settings**: All preferences are saved automatically

Access customization through the gear icon (⚙️) in the top-right corner of any note.

---

## 📁 Project Structure

```
Stickity_Stacks/
├── stickity_stacks.py              # Main application (Linux/GTK4)
├── stickity_stacks_win.py          # Windows version (tkinter)
├── build.bat                       # Windows executable builder
├── build_complete.bat              # Complete installer builder
├── build_installer.spec            # PyInstaller configuration
├── installer.iss                   # Inno Setup installer script
├── com.stickity.stacks.desktop     # Linux desktop integration
├── stickity_stacks.png             # Application icon
├── requirements_windows.txt        # Windows dependencies
├── snapcraft.yaml                  # Snap package configuration
├── README.md                       # This file
├── README_WINDOWS.md               # Windows-specific README
├── QUICKSTART.md                   # Beginner's guide
├── BUILD_INSTALLER.md              # Installer build guide
└── LICENSE                         # MIT License
```

---

## 🔧 Development

### Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add some amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Issues and Bug Reports

Found a bug or have a feature request? Please [open an issue](https://github.com/Hot-snakes/Stickity_Stacks/issues) on GitHub.

### Development Setup

**Linux:**
```bash
git clone https://github.com/Hot-snakes/Stickity_Stacks.git
cd Stickity_Stacks
sudo dnf install python3-gobject gtk4  # Fedora
python3 stickity_stacks.py
```

**Windows:**
```cmd
git clone https://github.com/Hot-snakes/Stickity_Stacks.git
cd Stickity_Stacks
python stickity_stacks_win.py
```

---

## 📦 Packaging

### Windows Installer
See [BUILD_INSTALLER.md](BUILD_INSTALLER.md) for complete instructions.

### Snap Package (Linux)
```bash
snapcraft
```

---

## 🔒 Data Storage

**Linux:**
- Notes stored in: `stickity_stacks_notes.json`

**Windows:**
- Notes stored in: `%USERPROFILE%\stickity_stacks_notes_win.json`

Files are automatically created and updated. Safe to delete if you want to reset all notes and settings.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Tyrrell Chartrand**
- GitHub: [@Hot-snakes](https://github.com/Hot-snakes)
- Email: mr0tstihs81@gmail.com

---

## 🙏 Acknowledgments

- Built with [GTK4](https://gtk.org/), [tkinter](https://docs.python.org/3/library/tkinter.html), and [Python](https://python.org/)
- Inspired by the need for simple, effective desktop note-taking
- Thanks to the GTK, tkinter, and Python communities for excellent documentation

---

## 🚀 Future Features

- [ ] Multiple note windows
- [ ] Note export functionality
- [ ] Reminder/alarm integration
- [ ] Cloud sync capabilities
- [ ] Plugin system for extensions
- [ ] macOS support

---

## 📚 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Perfect for beginners!
- **[Windows README](README_WINDOWS.md)** - Windows-specific details
- **[Build Installer Guide](BUILD_INSTALLER.md)** - How to build the Windows installer
- **[Main Documentation](README.md)** - You are here!

---

<div align="center">
  <strong>Happy note stacking! 📝✨</strong>
  
  ⭐ **Star this repo if you find it useful!** ⭐
</div>
