"""
calendar.py - Reminders & Local Calendar Scheduler Tools for JARVIS
"""
import os
import json
import time
import datetime
import threading
import logging
from typing import List, Dict
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from voice.text_to_speech import tts_engine
from config.constants import PermissionLevel

REMINDERS_FILE = os.path.join(os.path.expanduser("~"), ".jarvis", "reminders.json")

class ReminderScheduler:
    """Manages scheduled reminders and triggers notification alerts."""

    def __init__(self):
        self.reminders: List[Dict] = []
        self._load()
        self._thread = threading.Thread(target=self._checker_loop, daemon=True)
        self._thread.start()

    def _load(self):
        if os.path.exists(REMINDERS_FILE):
            try:
                with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
                    self.reminders = json.load(f)
            except Exception:
                self.reminders = []

    def _save(self):
        os.makedirs(os.path.dirname(REMINDERS_FILE), exist_ok=True)
        try:
            with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.reminders, f, indent=2)
        except Exception as e:
            logging.error(f"[ReminderScheduler] Save error: {e}")

    def add_reminder(self, text: str, time_str: str) -> str:
        rec = {
            "id": int(time.time()),
            "text": text,
            "time_str": time_str,
            "created_at": datetime.datetime.now().isoformat(),
            "triggered": False
        }
        self.reminders.append(rec)
        self._save()
        return f"Reminder set: '{text}' at {time_str}"

    def _checker_loop(self):
        while True:
            now_str = datetime.datetime.now().strftime("%H:%M")
            for r in self.reminders:
                if not r.get("triggered") and r.get("time_str") == now_str:
                    r["triggered"] = True
                    self._save()
                    msg = f"Reminder Alert: {r['text']}"
                    logging.info(f"[Reminder] {msg}")
                    tts_engine.speak(msg)
            time.sleep(20)

scheduler = ReminderScheduler()

class SetReminderTool(BaseTool):
    name = "set_reminder"
    description = "Set a timed reminder or calendar alert."
    parameters_schema = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Reminder text note"},
            "time_str": {"type": "string", "description": "Time string e.g. 19:00"}
        },
        "required": ["text"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, text: str, time_str: str = "19:00", **kwargs) -> ToolResult:
        res = scheduler.add_reminder(text, time_str)
        return ToolResult(True, res)

class GetCalendarTool(BaseTool):
    name = "get_calendar"
    description = "List set reminders and upcoming calendar events."
    parameters_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, **kwargs) -> ToolResult:
        if not scheduler.reminders:
            return ToolResult(True, "No reminders set for today.")

        items = [f"• [{r['time_str']}] {r['text']} ({'Done' if r['triggered'] else 'Pending'})" for r in scheduler.reminders]
        out = "\n".join(items)
        return ToolResult(True, f"Calendar & Reminders:\n{out}")

tool_registry.register(SetReminderTool())
tool_registry.register(GetCalendarTool())
