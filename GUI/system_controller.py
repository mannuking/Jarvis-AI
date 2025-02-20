import ctypes
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

class SystemController:
    def __init__(self):
        # Initialize audio controller
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(interface, POINTER(IAudioEndpointVolume))
        
    def set_volume(self, level: int) -> bool:
        """Set system volume (0-100)"""
        try:
            # Convert percentage to scalar value
            scalar = level / 100.0
            self.volume.SetMasterVolumeLevelScalar(scalar, None)
            return True
        except Exception as e:
            print(f"Error setting volume: {e}")
            return False
            
    def get_volume(self) -> int:
        """Get current volume level (0-100)"""
        try:
            return int(self.volume.GetMasterVolumeLevelScalar() * 100)
        except Exception as e:
            print(f"Error getting volume: {e}")
            return 0
            
    def set_brightness(self, level: int) -> bool:
        """Set screen brightness (0-100)"""
        try:
            sbc.set_brightness(level)
            return True
        except Exception as e:
            print(f"Error setting brightness: {e}")
            return False
            
    def get_brightness(self) -> int:
        """Get current brightness level (0-100)"""
        try:
            return sbc.get_brightness()[0]
        except Exception as e:
            print(f"Error getting brightness: {e}")
            return 0