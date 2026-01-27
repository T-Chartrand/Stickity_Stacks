# 🚀 Quick Start for Windows Users

**Never built software before? No problem!** This guide will walk you through installing Stickity Stacks in the easiest way possible.

---

## ⚡ Super Easy Method (Recommended)

### Step 1: Download the Installer

1. Go to the [Releases](https://github.com/Hot-snakes/Stickity_Stacks/releases) page
2. Download the file named: `StickityStacks_Setup_v1.0.0.exe`
3. Save it to your Downloads folder

### Step 2: Install

1. Find the downloaded file in your Downloads folder
2. **Double-click** the file
3. If Windows shows a warning:
   - Click "More info"
   - Click "Run anyway"
   - *(This is normal for new apps!)*
4. Follow the installation wizard:
   - Click "Next"
   - Choose where to install (default is fine)
   - Click "Install"
   - Click "Finish"

### Step 3: Start Using It!

- Find "Stickity Stacks" in your Start Menu
- Or double-click the desktop shortcut (if you chose to create one)
- Start creating sticky notes!

**That's it! You're done! 🎉**

---

## 🔧 Alternative: Run from Python (Slightly More Steps)

If the installer doesn't work or you want to run from source:

### What You Need
- **Python** (free software that runs the app)

### Step-by-Step

#### 1. Install Python

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button
3. Run the installer
4. **IMPORTANT:** Check the box "Add Python to PATH" ✅
5. Click "Install Now"
6. Wait for it to finish
7. Click "Close"

#### 2. Download Stickity Stacks

**Option A: Download as ZIP (Easier)**
1. Go to the [main page](https://github.com/Hot-snakes/Stickity_Stacks)
2. Click the green "Code" button
3. Click "Download ZIP"
4. Save the ZIP file
5. Right-click the ZIP file → "Extract All"
6. Choose where to extract (Downloads is fine)

**Option B: Use Git (If you know how)**
```cmd
git clone https://github.com/Hot-snakes/Stickity_Stacks.git
```

#### 3. Run the App

1. Open the folder where you extracted the files
2. Hold **Shift** and **right-click** in an empty area
3. Click "Open PowerShell window here" or "Open command window here"
4. Type this and press Enter:
   ```cmd
   python stickity_stacks_win.py
   ```
5. The app should start!

#### 4. Create a Desktop Shortcut (Optional)

1. Right-click `stickity_stacks_win.py`
2. Send to → Desktop (create shortcut)
3. Now you can double-click the shortcut to run the app!

---

## ❓ Troubleshooting for Beginners

### "Python is not recognized..."

**Problem:** Windows doesn't know where Python is.

**Solution:**
1. Uninstall Python
2. Reinstall Python
3. **Make sure** to check "Add Python to PATH" during installation ✅

### "The installer won't run"

**Problem:** Windows SmartScreen is protecting you.

**Solution:**
1. Click "More info" on the warning
2. Click "Run anyway"
3. This is normal for apps that aren't widely distributed yet

### "I get an error when running the Python script"

**Problem:** Missing dependencies or wrong Python version.

**Solution:**
1. Open Command Prompt
2. Run: `python --version`
3. Make sure it says Python 3.6 or higher
4. If not, install the latest Python

### "Nothing happens when I run the app"

**Problem:** The app might be running in the background.

**Solution:**
1. Check your system tray (bottom-right corner)
2. Look for the Stickity Stacks icon
3. Or press **Ctrl+N** to create a new note

### "I accidentally closed all my notes"

**Don't worry!** Your notes are auto-saved.

**Solution:**
1. Just restart the app
2. Your notes will reappear automatically!

---

## 🆘 Need More Help?

### Where to Get Help

1. **Read the full documentation:** [README_WINDOWS.md](README_WINDOWS.md)
2. **Check common issues:** [GitHub Issues](https://github.com/Hot-snakes/Stickity_Stacks/issues)
3. **Ask a question:** Create a new issue on GitHub
4. **Community:** Check if there's a Discord or forum (link in main README)

### What to Include When Asking for Help

To get help faster, include:
- What you were trying to do
- What happened instead
- Any error messages you saw
- Your Windows version (type `winver` in search)
- Screenshot of the error (if possible)

---

## 📚 Learning More

Want to understand what's happening behind the scenes?

- **Python:** The programming language the app is written in
  - [Learn Python](https://www.python.org/about/gettingstarted/)
  
- **Tkinter:** The library that creates the windows and buttons
  - Built into Python, no installation needed!
  
- **PyInstaller:** Converts Python scripts into .exe files
  - [PyInstaller Documentation](https://pyinstaller.org/)
  
- **Inno Setup:** Creates professional installers
  - [Inno Setup Website](https://jrsoftware.org/isinfo.php)

---

## 💡 Tips for Success

✅ **DO:**
- Read error messages carefully
- Google error messages you don't understand
- Ask for help if you're stuck
- Check if Python is in your PATH
- Keep backups of your notes file

❌ **DON'T:**
- Panic if something doesn't work the first time
- Skip the "Add to PATH" checkbox when installing Python
- Delete files you don't understand
- Modify the source code unless you know Python
- Ignore antivirus warnings without investigating

---

## 🎯 What to Do Next

### For Users
1. Install the app using the easiest method
2. Create your first sticky note
3. Customize the colors and fonts
4. Enjoy staying organized!

### For Curious Learners
1. Try running from Python to see how it works
2. Read the source code in `stickity_stacks_win.py`
3. Make small changes and see what happens
4. Learn Python to create your own apps!

### For Future Developers
1. Master the basics of running the app
2. Learn Python fundamentals
3. Study the source code to understand how it works
4. Try adding your own features!

---

## 📖 Glossary for Beginners

**Python:** A programming language (like English for computers)

**Script:** A file containing code that tells the computer what to do

**Terminal/Command Prompt/PowerShell:** A text-based way to control your computer

**PATH:** A list of folders where Windows looks for programs

**Executable (.exe):** A program file that runs on Windows

**Installer:** A program that installs another program

**Source Code:** The human-readable instructions that make a program work

**Repository (Repo):** A place where code is stored (like GitHub)

**ZIP:** A compressed file that contains other files

**Dependencies:** Other software that a program needs to run

---

## ✅ Checklist: "Did I Do It Right?"

After installing, verify everything works:

- [ ] The app starts when I double-click it
- [ ] I can create a new sticky note (Ctrl+N)
- [ ] I can type in the sticky note
- [ ] The note stays on screen when I type
- [ ] I can drag the note around
- [ ] I can resize the note
- [ ] When I close and restart the app, my notes come back
- [ ] I can delete notes (Ctrl+D or trash icon)
- [ ] I can change fonts and colors in settings

**All checked?** Congratulations, you're all set! 🎉

---

## 🌟 You Did It!

Welcome to Stickity Stacks! We hope you enjoy using it to stay organized.

**Remember:** Everyone was a beginner once. If you got stuck but figured it out, consider helping others by:
- Sharing what worked for you
- Improving this documentation
- Answering questions on GitHub

**Happy note-taking! 📝**

---

*Last updated: January 2026*
*For technical details, see [BUILD_INSTALLER.md](BUILD_INSTALLER.md)*
