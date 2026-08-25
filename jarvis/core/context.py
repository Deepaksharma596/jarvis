"""
context.py - Active Windows Environment Context Collector
"""
import datetime
import psutil
import logging

try:
    import win32gui
    import win32process
    HAS_WIN32 = True
except ImportError:
    HAS_WIN32 = False

class SystemContext:
    """Collects real-time context about the user's computer state."""

    @staticmethod
    def get_active_window_title() -> str:
        """Return title of currently focused application window."""
        if not HAS_WIN32:
            return "Unknown"
        try:
            hwnd = win32gui.GetForegroundWindow()
            title = win32gui.GetWindowText(hwnd)
            return title if title else "Desktop / No active window"
        except Exception as e:
            logging.warning(f"[Context] Error getting active window title: {e}")
            return "Unknown"

    @staticmethod
    def get_system_stats() -> dict:
        """Return CPU, Memory, Battery stats."""
        stats = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "ram_percent": psutil.virtual_memory().percent,
            "ram_available_gb": round(psutil.virtual_memory().available / (1024 ** 3), 2),
        }
        battery = psutil.sensors_battery()
        if battery:
            stats["battery_percent"] = battery.percent
            stats["power_plugged"] = battery.power_plugged
        else:
            stats["battery_percent"] = None
            stats["power_plugged"] = None
        return stats

    @classmethod
    def get_full_context_prompt(cls) -> str:
        """Format system context for AI Prompt."""
        now = datetime.datetime.now()
        active_window = cls.get_active_window_title()
        stats = cls.get_system_stats()
        
        ctx = f"Current Time: {now.strftime('%A, %B %d, %Y %I:%M %p')}\n"
        ctx += f"Active Window: {active_window}\n"
        ctx += f"CPU Usage: {stats['cpu_percent']}%, RAM Usage: {stats['ram_percent']}%"
        if stats["battery_percent"] is not None:
            status = "Plugged In" if stats["power_plugged"] else "On Battery"
            ctx += f", Battery: {stats['battery_percent']}% ({status})"
        return ctx
