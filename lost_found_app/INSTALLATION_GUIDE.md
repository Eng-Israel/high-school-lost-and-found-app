# Lost & Found System - Portable Installation Guide

## Overview
This guide explains how to set up the Lost & Found system on any Windows computer using the portable installation package.

## What's Included
- `install.bat` - Automated installation script
- `run.bat` - Quick start script to run the app
- `app.py` - Main application code
- `requirements.txt` - List of Python packages needed
- `templates/` - All HTML pages
- `static/css/` - Styling files
- Documentation files

## System Requirements
- **Windows 7 or newer** (XP/Vista may work but not tested)
- **Internet connection** (for downloading Python and dependencies)
- **Minimum 500 MB free disk space**
- **Administrator rights** (recommended for installation)

## Installation Steps

### Step 1: Prepare the Installation Files
1. Copy the entire Lost & Found folder to your computer (from flash drive)
2. Place it in a location like:
   - `C:\Program Files\LostFound`
   - `C:\Users\YourName\Documents\LostFound`
   - Or anywhere you prefer

### Step 2: Check Python Installation
1. Open Command Prompt (cmd.exe)
2. Type: `python --version`
3. If Python is installed, you'll see the version (e.g., Python 3.11.4)
4. If you get "command not found" or "python is not recognized":
   - Download Python from: https://www.python.org/downloads/
   - Run the installer
   - **IMPORTANT**: Check the box "Add Python to PATH" during installation
   - Restart your computer after installation

### Step 3: Run the Installer
1. Open File Explorer
2. Navigate to your Lost & Found folder
3. Double-click `install.bat`
4. A command window will open and:
   - Check for Python ✓
   - Create a virtual environment
   - Download and install all dependencies (Flask, SQLAlchemy, etc.)
   - Initialize the database
   - Optionally start the application

**Note**: The first installation may take 2-3 minutes as it downloads packages.

### Step 4: Start the Application
You have two options:

**Option A - After Installation (Recommended)**
- The installer asks if you want to start the app immediately
- Click `y` and press Enter
- The app will open automatically

**Option B - Manual Start**
- Double-click `run.bat` in the Lost & Found folder
- Or open Command Prompt and type:
  ```
  cd C:\path\to\lost_found_app
  python app.py
  ```

### Step 5: Access the Application
1. Once the app is running, your browser will automatically open
2. Go to: `http://127.0.0.1:5000`
3. Click "Setup System" to create the initial admin account
4. Follow the setup wizard

## Troubleshooting

### Problem: "Python is not installed or not in PATH"
**Solution:**
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **Uncheck** "Install for all users"
4. **Check** "Add Python to PATH"
5. Click "Install Now"
6. Restart your computer
7. Try running `install.bat` again

### Problem: "Failed to install dependencies"
**Solution:**
1. Check your internet connection
2. Run `install.bat` again
3. If still failing, open Command Prompt and run:
   ```
   .venv\Scripts\activate.bat
   pip install Flask Flask-SQLAlchemy --upgrade
   ```

### Problem: "Address already in use"
**Solution:**
1. Close any other running instances of the app
2. Wait 30 seconds
3. Run `run.bat` again
4. Or change the port in `app.py` line: `app.run(debug=True, port=5001)`

### Problem: Database errors
**Solution:**
1. Close the app
2. Delete the `instance` folder
3. Run `run.bat` again
4. The database will be recreated

## Advanced Usage

### Creating a Shortcut
1. Right-click `run.bat`
2. Select "Send to" > "Desktop (create shortcut)"
3. You can now start the app with a desktop icon

### Running on a Different Port
1. Open `app.py` in a text editor
2. Find the line: `app.run(debug=True, port=5000)`
3. Change `5000` to any unused port (e.g., `8080`)
4. Save and run `run.bat`

### Uninstalling
1. Close the application
2. Delete the entire Lost & Found folder
3. No registry entries or hidden files are created

## File Structure Explained
```
lost_found_app/
├── install.bat              ← Run this first (installation)
├── run.bat                  ← Run this to start the app
├── app.py                   ← Main application code
├── requirements.txt         ← List of dependencies
├── templates/               ← HTML pages
├── static/css/              ← Styling
├── instance/                ← Database (created after first run)
└── .venv/                   ← Virtual environment (created during install)
```

## Regular Usage (After Installation)

### Daily Startup
1. Double-click `run.bat`
2. Wait for browser to open (usually instant)
3. Go to http://127.0.0.1:5000

### First-Time Setup Only
1. Run the app
2. Click "Setup System"
3. Create admin account
4. System is ready to use

### Backing Up Your Data
The database file is located at:
```
instance/lost_found.db
```
To backup your data:
1. Close the app
2. Copy the `instance` folder to a safe location
3. To restore, replace the `instance` folder and restart

## Getting Help

### Check Logs
When the app is running, error messages appear in the Command Prompt window.
Take a screenshot and save it for troubleshooting.

### Manual Database Reset
If you want to start fresh:
1. Close the app
2. Delete `instance/lost_found.db`
3. Run the app again
4. Re-run setup

## Support for Installation Issues

If you encounter issues:
1. Note the exact error message
2. Check the troubleshooting section above
3. Ensure Python is properly installed
4. Check that you have internet access during installation
5. Try running as Administrator

---

**Version**: 1.0
**Last Updated**: April 2026
**Compatible with**: Windows 7 and newer
