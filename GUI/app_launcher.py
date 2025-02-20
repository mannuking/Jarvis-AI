import os
import shutil
import winreg
import subprocess
import psutil
import json
from typing import Optional

class AppLauncher:
    def __init__(self, aliases_file="app_aliases.json"):
        self.load_aliases(aliases_file)
        
    def load_aliases(self, aliases_file):
        try:
            with open(aliases_file, 'r') as f:
                self.app_aliases = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Aliases file '{aliases_file}' not found. Using default aliases.")
            self.app_aliases = {
                "chrome": ["google chrome", "google", "browser"],
                "whatsapp": ["whatsapp messenger", "whatsapp desktop"],
                "vscode": ["visual studio code", "vs code", "code"],
                "word": ["microsoft word", "ms word", "winword"],
                "excel": ["microsoft excel", "ms excel"],
                "powerpoint": ["microsoft powerpoint", "ms powerpoint", "ppt"],
                "notepad": ["notes", "text editor"],
                "cmd": ["command prompt", "terminal", "command line"],
                "calculator": ["calc"],
                "task manager": ["taskman", "tasks"]
            }
            # Save default aliases to file for future use
            try:
                with open(aliases_file, 'w') as f:
                    json.dump(self.app_aliases, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not save default aliases to file: {e}")

    def _is_process_running(self, process_name):
        """Check if a process is already running"""
        for proc in psutil.process_iter(['name']):
            try:
                if process_name.lower() in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return False

    def find_app_in_registry(self, app_name):
        """Search for application in Windows Registry"""
        try:
            # Try with and without .exe extension
            possible_names = [app_name]
            if not app_name.lower().endswith('.exe'):
                possible_names.append(f"{app_name}.exe")

            for name in possible_names:
                try:
                    # Check App Paths
                    key_path = f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths\\{name}"
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, 
                                       winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
                    path = winreg.QueryValue(key, None)
                    winreg.CloseKey(key)
                    if path and os.path.exists(path):
                        return path
                except WindowsError:
                    # Try 32-bit registry
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0,
                                           winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
                        path = winreg.QueryValue(key, None)
                        winreg.CloseKey(key)
                        if path and os.path.exists(path):
                            return path
                    except WindowsError:
                        continue
        except Exception as e:
            print(f"Registry search error: {e}")
        return None

    def find_app(self, app_name: str) -> Optional[str]:
        """Find application path using multiple methods"""
        app_name = app_name.lower().strip()

        # Check aliases first
        for main_app, aliases in self.app_aliases.items():
            if app_name in aliases or app_name == main_app:
                app_name = main_app
                break

        # Debugging prints
        print(f"Finding app: {app_name}")

        # 1. Try shutil.which (fastest)
        print("Trying shutil.which...")
        path_which = shutil.which(app_name)
        if path_which:
            print(f"shutil.which found: {path_which}")
            return path_which
        
        path_which_exe = shutil.which(app_name + ".exe")
        if path_which_exe:
            print(f"shutil.which found (with .exe): {path_which_exe}")
            return path_which_exe

        # 2. Try Registry Search
        print("Trying Registry Search...")
        path_registry = self.find_app_in_registry(app_name)
        if path_registry:
            print(f"Registry Search found: {path_registry}")
            return path_registry

        # 3. Special handling for system apps
        print("Checking system apps...")
        system_apps = {
            'calculator': 'calc.exe',
            'camera': 'microsoft.windows.camera:',
            'paint': 'mspaint.exe',
            'task manager': 'taskmgr.exe',
            'control panel': 'control.exe'
        }
        
        if app_name in system_apps:
            return system_apps[app_name]

        return None

    def launch_app(self, app_name: str) -> bool:
        """Launch application by name"""
        try:
            # Special handling for camera
            if 'camera' in app_name.lower():
                subprocess.run('start microsoft.windows.camera:', shell=True)
                return True

            path = self.find_app(app_name)
            if not path:
                print(f"Could not find {app_name}")
                return False

            process_name = os.path.basename(path) if path else app_name
            if self._is_process_running(process_name):
                print(f"{app_name} is already running")
                return True

            if ':' in path:  # Special URI handling (like camera)
                subprocess.run(f'start {path}', shell=True)
            elif path.endswith('.exe'):
                os.startfile(path)
            else:
                subprocess.run(path, shell=True)
            return True

        except Exception as e:
            print(f"Error launching {app_name}: {e}")
            return False

    def force_launch(self, app_name: str) -> bool:
        """Force launch an application using shell commands"""
        try:
            subprocess.run(f'start {app_name}', shell=True)
            return True
        except Exception as e:
            print(f"Force launch failed: {e}")
            return False
