"""
windows.py - Native Windows UI Automation & Application Registry Discovery
"""
import os
import glob
import subprocess
import webbrowser
import logging
from typing import Dict, Optional, List

try:
    import win32gui
    import win32con
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class AppRegistry:
    """Discovers installed Windows desktop applications and executable paths."""

    COMMON_PATHS = [
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe",
        r"C:\Program Files\Microsoft VS Code\Code.exe",
        r"C:\Users\%USERNAME%\AppData\Local\WhatsApp\WhatsApp.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Programs\WhatsApp\WhatsApp.exe",
        r"C:\Users\%USERNAME%\AppData\Local\Microsoft\WindowsApps\WhatsApp.exe",
        r"C:\Program Files\WhatsApp\WhatsApp.exe",
        r"C:\Windows\System32\notepad.exe",
        r"C:\Windows\System32\calc.exe",
        r"C:\Windows\System32\cmd.exe",
        r"C:\Windows\explorer.exe",
    ]

    def __init__(self):
        self.apps: Dict[str, str] = {}
        self._scan_common_paths()
        self._scan_start_menu()

    def _scan_common_paths(self):
        user = os.environ.get("USERNAME", "")
        for path in self.COMMON_PATHS:
            expanded = path.replace("%USERNAME%", user)
            if os.path.exists(expanded):
                basename = os.path.basename(expanded).lower().replace(".exe", "")
                self.apps[basename] = expanded
                if basename == "code":
                    self.apps["vscode"] = expanded
                    self.apps["vs code"] = expanded
                if basename == "msedge":
                    self.apps["edge"] = expanded

    def _scan_start_menu(self):
        start_menu_dirs = [
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
            os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
        ]
        for sdir in start_menu_dirs:
            if os.path.exists(sdir):
                for shortcut in glob.glob(os.path.join(sdir, "**", "*.lnk"), recursive=True):
                    name = os.path.basename(shortcut).lower().replace(".lnk", "")
                    self.apps[name] = shortcut

    def find_app_path(self, name: str) -> Optional[str]:
        """Lookup executable or shortcut path for given app name."""
        name_clean = name.lower().strip()
        if name_clean in self.apps:
            return self.apps[name_clean]

        # Substring fuzzy search
        for app_key, app_path in self.apps.items():
            if name_clean in app_key or app_key in name_clean:
                return app_path

        return None

class WindowsAutomation:
    """Helper for Windows window manipulation (Focus, Switch, Minimize, Maximize, Close)."""

    @staticmethod
    def launch_app(app_path_or_name: str) -> bool:
        """Launch application executable or protocol URL safely."""
        name_lower = app_path_or_name.lower().strip()

        # 1. Special protocol handling (e.g. WhatsApp UWP app)
        if name_lower == "whatsapp" or name_lower.startswith("whatsapp://"):
            try:
                os.startfile("whatsapp://")
                return True
            except Exception:
                try:
                    webbrowser.open("whatsapp://")
                    return True
                except Exception:
                    pass

        # 2. File path or executable
        if os.path.exists(app_path_or_name):
            try:
                os.startfile(app_path_or_name)
                return True
            except Exception:
                pass

        # 3. Windows Start command fallback (prevents 'not recognized as internal/external command' crash)
        try:
            subprocess.Popen(f'start "" "{app_path_or_name}"', shell=True)
            return True
        except Exception as e:
            logging.error(f"[WindowsAutomation] Failed to launch '{app_path_or_name}': {e}")
            return False

    @staticmethod
    def find_window_by_title(title_substring: str) -> List[int]:
        """Find window handles matching title substring."""
        if not HAS_WIN32:
            return []
        matches = []

        def enum_handler(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                txt = win32gui.GetWindowText(hwnd)
                if title_substring.lower() in txt.lower():
                    matches.append(hwnd)

        win32gui.EnumWindows(enum_handler, None)
        return matches

    @classmethod
    def focus_window(cls, title_substring: str) -> bool:
        """Bring window matching title to foreground."""
        hwnds = cls.find_window_by_title(title_substring)
        if not hwnds or not HAS_WIN32:
            return False
        try:
            hwnd = hwnds[0]
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(hwnd)
            return True
        except Exception as e:
            logging.error(f"[WindowsAutomation] Focus window error: {e}")
            return False

    @classmethod
    def close_window(cls, title_substring: str) -> bool:
        """Close window matching title."""
        hwnds = cls.find_window_by_title(title_substring)
        if not hwnds or not HAS_WIN32:
            return False
        try:
            for hwnd in hwnds:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            return True
        except Exception as e:
            logging.error(f"[WindowsAutomation] Close window error: {e}")
            return False

# Global Singleton App Registry
app_registry = AppRegistry()
