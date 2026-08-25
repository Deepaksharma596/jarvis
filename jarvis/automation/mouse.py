"""
mouse.py - Safe Mouse Input Automation Wrapper
"""
import time
import logging
from config.settings import settings

try:
    import pyautogui
    HAS_PYAUTOGUI = True
    pyautogui.FAILSAFE = True  # Move mouse to upper-left corner to abort
except ImportError:
    HAS_PYAUTOGUI = False

class MouseAutomation:
    """Safe Mouse Automation helper functions."""

    @staticmethod
    def move(x: int, y: int):
        if HAS_PYAUTOGUI and not settings.mock_mode:
            pyautogui.moveTo(x, y, duration=settings.automation_speed)

    @staticmethod
    def click(x: int = None, y: int = None, button: str = "left", clicks: int = 1):
        if HAS_PYAUTOGUI and not settings.mock_mode:
            pyautogui.click(x=x, y=y, clicks=clicks, button=button, interval=0.1)
            time.sleep(settings.automation_speed)

    @staticmethod
    def double_click(x: int = None, y: int = None):
        MouseAutomation.click(x=x, y=y, button="left", clicks=2)

    @staticmethod
    def right_click(x: int = None, y: int = None):
        MouseAutomation.click(x=x, y=y, button="right", clicks=1)

    @staticmethod
    def scroll(clicks: int):
        if HAS_PYAUTOGUI and not settings.mock_mode:
            pyautogui.scroll(clicks)
