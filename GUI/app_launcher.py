import os
import subprocess
import json

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
                "chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "whatsapp": "C:\\Users\\%USERNAME%\\AppData\\Local\\WhatsApp\\WhatsApp.exe",
                "vscode": "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
                "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE",
                "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
                "notepad": "notepad.exe",
                "cmd": "cmd.exe",
                "calculator": "calc.exe",
                "task manager": "taskmgr.exe",
                "camera": "microsoft.windows.camera:",
                "control panel": "control.exe",
                "paint": "mspaint.exe"
            }

    def launch_app(self, app_name: str) -> bool:
        """Launch application by name"""
        try:
            app_name = app_name.lower().strip()
            
            # Handle system apps first
            system_apps = {
                'calculator': 'calc.exe',
                'camera': 'microsoft.windows.camera:',
                'paint': 'mspaint.exe',
                'task manager': 'taskmgr.exe',
                'notepad': 'notepad.exe',
                'cmd': 'cmd.exe',
                'command prompt': 'cmd.exe',
                'control panel': 'control.exe'
            }
            
            if app_name in system_apps:
                subprocess.run(system_apps[app_name], shell=True)
                return True
                
            # Try to launch from app_aliases
            if app_name in self.app_aliases:
                path = os.path.expandvars(self.app_aliases[app_name])
                if os.path.exists(path):
                    os.startfile(path)
                    return True
            
            # If no direct match, try force launch
            return self.force_launch(app_name)

        except Exception as e:
            print(f"Error launching {app_name}: {e}")
            return False

    def force_launch(self, app_name: str) -> bool:
        """Force launch an application using shell command"""
        try:
            subprocess.run(f'start {app_name}', shell=True)
            return True
        except Exception as e:
            print(f"Force launch failed: {e}")
            return False
