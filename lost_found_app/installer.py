"""
Lost & Found System - Python Installer (Alternative to install.bat)
Run this script if install.bat doesn't work on your system

Usage:
    python installer.py
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*50)
    print(f"  {text}")
    print("="*50 + "\n")

def check_python():
    """Verify Python is properly installed"""
    print_header("Checking Python Installation")
    version = sys.version
    print(f"Python version: {version}")
    print(f"Executable: {sys.executable}")
    print("[OK] Python is properly installed\n")
    return True

def create_venv():
    """Create virtual environment"""
    print_header("Creating Virtual Environment")
    
    venv_path = Path(".venv")
    if venv_path.exists():
        print("[OK] Virtual environment already exists\n")
        return True
    
    print("[*] Creating .venv folder...")
    try:
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
        print("[OK] Virtual environment created successfully\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to create virtual environment: {e}\n")
        return False

def get_pip_path():
    """Get the path to pip in the virtual environment"""
    if sys.platform == "win32":
        return Path(".venv/Scripts/pip.exe")
    else:
        return Path(".venv/bin/pip")

def get_python_path():
    """Get the path to python in the virtual environment"""
    if sys.platform == "win32":
        return Path(".venv/Scripts/python.exe")
    else:
        return Path(".venv/bin/python")

def upgrade_pip():
    """Upgrade pip in virtual environment"""
    print_header("Upgrading pip")
    
    pip_path = get_pip_path()
    if not pip_path.exists():
        print("[WARNING] pip not found in virtual environment\n")
        return False
    
    print("[*] Upgrading pip...")
    try:
        subprocess.run([str(pip_path), "install", "--upgrade", "pip"], 
                      capture_output=True, check=True)
        print("[OK] pip upgraded successfully\n")
        return True
    except subprocess.CalledProcessError:
        print("[WARNING] Could not upgrade pip, continuing anyway...\n")
        return True

def install_requirements():
    """Install required packages"""
    print_header("Installing Dependencies")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("[ERROR] requirements.txt not found\n")
        return False
    
    pip_path = get_pip_path()
    if not pip_path.exists():
        print("[ERROR] pip not found in virtual environment\n")
        return False
    
    print("[*] Installing packages from requirements.txt...")
    print("[*] This may take 1-2 minutes on first install...\n")
    
    try:
        result = subprocess.run(
            [str(pip_path), "install", "-r", "requirements.txt"],
            capture_output=False
        )
        
        if result.returncode == 0:
            print("\n[OK] All dependencies installed successfully\n")
            return True
        else:
            print("\n[ERROR] Failed to install dependencies")
            print("[*] Please check your internet connection and try again\n")
            return False
            
    except Exception as e:
        print(f"\n[ERROR] Installation failed: {e}\n")
        return False

def init_database():
    """Initialize the database"""
    print_header("Initializing Database")
    
    python_path = get_python_path()
    if not python_path.exists():
        print("[ERROR] Python not found in virtual environment\n")
        return False
    
    print("[*] Creating database...")
    try:
        subprocess.run(
            [str(python_path), "-c", 
             "from app import app, db; app.app_context().push(); db.create_all(); print('[OK] Database initialized')"],
            check=True
        )
        print("[OK] Database ready\n")
        return True
    except subprocess.CalledProcessError:
        print("[WARNING] Database initialization had an issue, app may still work\n")
        return True

def run_app():
    """Run the application"""
    print_header("Starting Application")
    
    python_path = get_python_path()
    if not python_path.exists():
        print("[ERROR] Python not found in virtual environment\n")
        return False
    
    print("[*] Starting Lost & Found System...")
    print("[*] Browser will open automatically at http://127.0.0.1:5000\n")
    
    try:
        subprocess.run([str(python_path), "app.py"])
        return True
    except Exception as e:
        print(f"[ERROR] Failed to start app: {e}\n")
        return False

def main():
    """Main installation flow"""
    print("\n")
    print("╔═══════════════════════════════════════╗")
    print("║  Lost & Found System Installer        ║")
    print("║  Python Version                       ║")
    print("╚═══════════════════════════════════════╝")
    
    # Check Python
    if not check_python():
        print("[ERROR] Python check failed")
        sys.exit(1)
    
    # Create virtual environment
    if not create_venv():
        print("[ERROR] Virtual environment creation failed")
        sys.exit(1)
    
    # Upgrade pip
    upgrade_pip()
    
    # Install requirements
    if not install_requirements():
        print("[ERROR] Dependency installation failed")
        print("Please check your internet connection and try again")
        sys.exit(1)
    
    # Initialize database
    init_database()
    
    # Ask if user wants to run app
    print_header("Installation Complete!")
    print("The Lost & Found System is ready to use.\n")
    
    response = input("Do you want to start the application now? (yes/no): ").strip().lower()
    
    if response in ['y', 'yes']:
        run_app()
    else:
        print("\nTo start the app later, run: python app.py")
        print("Or double-click run.bat\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Installation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        sys.exit(1)
