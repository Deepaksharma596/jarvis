"""
keyboard.py - Safe Keyboard Automation Wrapper
"""
import time
import logging
from config.settings import settings

try:
    import pyautogui
    HAS_PYAUTOGUI = True
except ImportError:
    HAS_PYAUTOGUI = False

class KeyboardAutomation:
    """Safe Keyboard Automation helper functions."""

    @staticmethod
    def type_text(text: str, interval: float = 0.02):
        if HAS_PYAUTOGUI and not settings.mock_mode:
            pyautogui.write(text, interval=interval)
            time.sleep(settings.automation_speed)

    @staticmethod
    def press_key(key: str):
        if HAS_PYAUTOGUI and not settings.mock_mode:
            pyautogui.press(key)
            time.sleep(settings.automation_speed)

    @staticmethod
    def hotkey(*keys):
        if HAS_PYAUTOGUI and not settings.mock_mode:
            pyautogui.hotkey(*keys)
            time.sleep(settings.automation_speed)
