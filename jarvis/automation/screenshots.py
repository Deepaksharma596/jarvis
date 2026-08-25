"""
screenshots.py - Screen Capture and Visual Locator Helpers
"""
import os
import tempfile
import logging

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

class ScreenCapture:
    """Captures desktop screenshots for analysis or visual UI verification."""

    @staticmethod
    def capture_to_file(save_path: str = None) -> str:
        """Capture screenshot and save to disk."""
        if not save_path:
            save_dir = os.path.join(os.path.expanduser("~"), ".jarvis", "screenshots")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, f"screenshot_{int(os.path.getmtime(__file__))}.png")

        if HAS_PYAUTOGUI:
            img = pyautogui.screenshot()
            img.save(save_path)
            logging.info(f"[ScreenCapture] Saved screenshot to {save_path}")
            return save_path

        return ""
