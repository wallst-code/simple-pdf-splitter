"""
Create desktop shortcuts for Simple PDF Splitter.
Creates shortcuts on Windows desktop with custom icon.
"""

import os
import sys
from pathlib import Path

def create_windows_shortcut():
    """Create a Windows desktop shortcut with custom icon."""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "Simple PDF Splitter.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(path)
        
        # Point to the Python script
        app_path = Path(__file__).parent / "main.py"
        python_exe = sys.executable
        
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{app_path}"'
        shortcut.WorkingDirectory = str(Path(__file__).parent)
        shortcut.Description = "Simple PDF Splitter - Split PDFs privately and reliably"
        
        # Set custom icon
        icon_path = Path(__file__).parent / "static" / "images" / "app_icon.ico"
        if icon_path.exists():
            shortcut.IconLocation = str(icon_path)
            print(f"[OK] Using custom icon: {icon_path.name}")
        else:
            print("[WARNING] Icon not found, using default Python icon")
            shortcut.IconLocation = python_exe
        
        shortcut.save()
        print(f"[SUCCESS] Desktop shortcut created: {path}")
        return True
        
    except ImportError:
        print("[ERROR] Required packages not installed.")
        print("Please run: pip install pywin32 winshell")
        return False
    except Exception as e:
        print(f"[ERROR] Failed to create shortcut: {e}")
        return False

def create_batch_launcher():
    """Create a batch file launcher as backup option."""
    try:
        # Try multiple desktop locations
        possible_desktops = [
            Path.home() / "Desktop",
            Path.home() / "OneDrive" / "Desktop",
            Path("C:/Users") / os.getlogin() / "Desktop"
        ]
        
        desktop = None
        for desk_path in possible_desktops:
            if desk_path.exists():
                desktop = desk_path
                break
        
        if not desktop:
            print("[ERROR] Could not find Desktop folder")
            return False
            
        batch_file = desktop / "Simple PDF Splitter.bat"
        
        # Create batch file content
        app_dir = Path(__file__).parent
        app_path = app_dir / "main.py"
        icon_path = app_dir / "static" / "images" / "app_icon.ico"
        
        batch_content = f"""@echo off
title Simple PDF Splitter
cd /d "{app_dir}"
echo Starting Simple PDF Splitter...
echo.
python "{app_path}"
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start Simple PDF Splitter
    echo Make sure Python is installed and in your PATH
    pause
)
"""
        
        with open(batch_file, 'w') as f:
            f.write(batch_content)
        
        print(f"[SUCCESS] Batch launcher created: {batch_file}")
        print("[TIP] You can right-click the .bat file to create a shortcut with custom icon")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to create batch file: {e}")
        return False

def create_start_menu_entry():
    """Create a Start Menu entry (Windows)."""
    try:
        import winshell
        from win32com.client import Dispatch
        
        start_menu = winshell.start_menu()
        programs_folder = Path(start_menu) / "Programs" / "Simple PDF Splitter"
        programs_folder.mkdir(exist_ok=True)
        
        path = programs_folder / "Simple PDF Splitter.lnk"
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(path))
        
        app_path = Path(__file__).parent / "main.py"
        python_exe = sys.executable
        
        shortcut.Targetpath = python_exe
        shortcut.Arguments = f'"{app_path}"'
        shortcut.WorkingDirectory = str(Path(__file__).parent)
        shortcut.Description = "Simple PDF Splitter - Split PDFs privately and reliably"
        
        # Set custom icon
        icon_path = Path(__file__).parent / "static" / "images" / "app_icon.ico"
        if icon_path.exists():
            shortcut.IconLocation = str(icon_path)
        
        shortcut.save()
        print(f"[SUCCESS] Start Menu entry created")
        return True
        
    except Exception as e:
        print(f"[WARNING] Could not create Start Menu entry: {e}")
        return False

def create_mac_app_launcher():
    """Create a Mac .command file launcher."""
    try:
        desktop = Path.home() / "Desktop"
        launcher_file = desktop / "Simple PDF Splitter.command"
        
        # Create launcher script
        app_dir = Path(__file__).parent
        app_path = app_dir / "main.py"
        
        launcher_content = f"""#!/bin/bash
# Simple PDF Splitter Launcher

cd "{app_dir}"
echo "Starting Simple PDF Splitter..."
echo "The application will open in your browser at http://localhost:5000"
echo ""
python3 "{app_path}"

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to start Simple PDF Splitter"
    echo "Make sure Python 3 is installed"
    read -p "Press Enter to exit..."
fi
"""
        
        with open(launcher_file, 'w') as f:
            f.write(launcher_content)
        
        # Make it executable
        os.chmod(launcher_file, 0o755)
        
        print(f"[SUCCESS] Mac launcher created: {launcher_file}")
        print("[TIP] Double-click the .command file to run")
        print("[TIP] You can drag it to your Dock for easy access")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to create Mac launcher: {e}")
        return False

def create_mac_instructions():
    """Print instructions for Mac users to create an app bundle."""
    print("\n" + "-"*50)
    print("Mac App Creation Instructions:")
    print("-"*50)
    print("\nTo create a proper Mac app with icon:")
    print("1. Open 'Automator' (search in Spotlight)")
    print("2. Choose 'Application' as document type")
    print("3. Add 'Run Shell Script' action")
    print("4. Paste this command:")
    print(f"   cd {Path(__file__).parent}")
    print(f"   python3 main.py")
    print("5. Save as 'Simple PDF Splitter' to Applications folder")
    print("6. Right-click the app → Get Info → drag icon to top-left icon")
    print("\nThe app will then be available in Launchpad and Applications")

def main():
    """Main function to create shortcuts."""
    print("\n" + "="*50)
    print("Simple PDF Splitter - Shortcut Creator")
    print("="*50)
    
    if sys.platform == 'win32':
        # Windows setup
        handle_windows_setup()
    elif sys.platform == 'darwin':
        # Mac setup
        handle_mac_setup()
    else:
        # Linux
        print("[INFO] For Linux, create a .desktop file or alias")
        print(f"[INFO] Application path: {Path(__file__).parent / 'main.py'}")
        return

def handle_windows_setup():
    """Handle Windows shortcut creation."""
    # Check for icon
    icon_path = Path(__file__).parent / "static" / "images" / "app_icon.ico"
    if icon_path.exists():
        print(f"[OK] Icon found: {icon_path.name}")
    else:
        print("[WARNING] Icon file not found")
    
    print("\nCreating shortcuts...")
    print("-" * 30)
    
    # Try to create Windows shortcut
    success = create_windows_shortcut()
    
    # Always create batch file as backup
    if not success:
        print("\nCreating alternative launcher...")
        create_batch_launcher()
    
    # Try Start Menu
    if success:
        print("\nCreating Start Menu entry...")
        create_start_menu_entry()
    
    print("\n" + "="*50)
    print("Setup Complete!")
    print("="*50)
    print("\nTo run Simple PDF Splitter:")
    print("  • Double-click the desktop shortcut")
    print("  • Or find it in the Start Menu")
    print("  • The app will open in your browser")
    
    input("\nPress Enter to exit...")

def handle_mac_setup():
    """Handle Mac launcher creation."""
    print("\nCreating Mac launcher...")
    print("-" * 30)
    
    # Create .command file
    success = create_mac_app_launcher()
    
    if success:
        # Show additional instructions
        create_mac_instructions()
    
    print("\n" + "="*50)
    print("Setup Complete!")
    print("="*50)
    print("\nTo run Simple PDF Splitter:")
    print("  • Double-click the .command file on your Desktop")
    print("  • Or follow the Automator instructions above for a proper app")
    print("  • The app will open in your browser at http://localhost:5000")

if __name__ == "__main__":
    main()