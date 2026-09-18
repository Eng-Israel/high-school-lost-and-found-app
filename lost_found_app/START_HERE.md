# 🎓 Lost & Found System

## Quick Start - Installation in 3 Steps

### ✅ What You Need
- Windows 7 or newer
- Internet connection (for downloading Python if needed)
- 500 MB disk space

### 🚀 Installation

**Step 1:** Double-click `install.bat`
- This will automatically:
  - Check for Python (or guide you to install it)
  - Download all required packages
  - Set up the database
  - Start the application

**Step 2:** Wait for installation to complete (2-3 minutes first time)

**Step 3:** Follow the setup wizard in your browser
- Create an admin account
- System is ready to use!

### 📖 After Installation

To run the app daily, simply double-click `run.bat`

---

## 📚 Documentation

- `INSTALLATION_GUIDE.md` - Detailed installation and troubleshooting
- `Lost_Found_App_Project_Report.md` - Full project documentation
- `Lost_Found_App_Engineer_Documentation.md` - Technical details for developers

---

## 🌟 Features

- ✓ Admin dashboard for managing found items
- ✓ Student lost item reporting and search
- ✓ Automatic matching of lost reports to found items
- ✓ Public display of available items
- ✓ Shelf/location tracking
- ✓ Dynamic item categories with flexible descriptions

---

## ⚙️ System Requirements

| Requirement | Details |
|-------------|---------|
| Operating System | Windows 7 or newer |
| Python | 3.7 or newer (auto-install guided) |
| Internet | Required during first installation |
| Disk Space | 500 MB minimum |
| RAM | 512 MB minimum |

---

## 🆘 Troubleshooting

**App won't start?**
1. Check Python is installed: `python --version` in Command Prompt
2. Run `install.bat` again
3. See `INSTALLATION_GUIDE.md` for detailed help

**Can't find port 5000?**
- Close any other instances of the app
- Wait 30 seconds
- Try again or change port in `app.py`

**Database errors?**
- Delete the `instance` folder
- Run the app again
- Database will be recreated

---

## 📁 File Layout

```
lost_found_app/
├── install.bat                    ← Start here (installation)
├── run.bat                        ← Daily startup shortcut
├── README.md                      ← This file
├── INSTALLATION_GUIDE.md          ← Full setup guide
├── app.py                         ← Application code
├── requirements.txt               ← Dependencies
├── templates/                     ← Web pages
├── static/css/                    ← Styling
└── instance/                      ← Database (created after install)
```

---

## 🔐 Security Notes

- Admin credentials are stored in the database
- For production use, enable password hashing
- Change the default `SECRET_KEY` in `app.py`
- Backup `instance/lost_found.db` regularly

---

## 💡 Tips

1. **Faster Startup**: Create a desktop shortcut to `run.bat`
2. **Mobile Access**: Share IP address with students (on same network)
3. **Backup**: Copy the `instance` folder to backup data
4. **Uninstall**: Simply delete the folder (no registry entries)

---

## 📝 Default Admin Setup

During first run, you'll create an admin account with:
- Username (your choice)
- Password (your choice)

The system pre-populates 30+ item types (uniforms, books, phones, etc.)

---

## 🎯 Next Steps After Installation

1. Run `install.bat` or `run.bat`
2. Go to http://127.0.0.1:5000
3. Click "Setup System" (first time only)
4. Create admin account
5. Add found items via admin dashboard
6. Students can report lost items

---

**Version**: 1.0 | **Date**: April 2026 | **Status**: Ready for Use

For more information, see `INSTALLATION_GUIDE.md`
