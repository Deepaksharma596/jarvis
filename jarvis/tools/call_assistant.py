"""
call_assistant.py - Missed Call & Caller Message Recorder with Availability Briefing
"""
import os
import json
import time
import datetime
import logging
from typing import List, Dict
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from voice.text_to_speech import tts_engine
from config.constants import PermissionLevel

MISSED_CALLS_FILE = os.path.join(os.path.expanduser("~"), ".jarvis", "missed_calls.json")

class CallAssistantManager:
    """Tracks missed calls, captures caller messages, and briefs the user upon availability."""

    def __init__(self):
        self.missed_calls: List[Dict] = []
        self._load()

    def _load(self):
        if os.path.exists(MISSED_CALLS_FILE):
            try:
                with open(MISSED_CALLS_FILE, "r", encoding="utf-8") as f:
                    self.missed_calls = json.load(f)
            except Exception:
                self.missed_calls = []

    def _save(self):
        os.makedirs(os.path.dirname(MISSED_CALLS_FILE), exist_ok=True)
        try:
            with open(MISSED_CALLS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.missed_calls, f, indent=2)
        except Exception as e:
            logging.error(f"[CallAssistant] Save error: {e}")

    def record_missed_call(self, caller: str, message: str = "") -> str:
        """Record a missed call event and caller message."""
        now = datetime.datetime.now().strftime("%I:%M %p")
        rec = {
            "id": int(time.time()),
            "caller": caller,
            "message": message if message else "No message left.",
            "time": now,
            "timestamp": datetime.datetime.now().isoformat(),
            "briefed": False
        }
        self.missed_calls.append(rec)
        self._save()
        logging.info(f"[CallAssistant] Recorded missed call from '{caller}' with message: '{message}'")
        return f"Recorded missed call from {caller}."

    def get_unread_briefing(self) -> str:
        """Generate voice & text briefing for unread missed calls."""
        unread = [c for c in self.missed_calls if not c.get("briefed")]
        if not unread:
            return "Welcome back! You have no missed calls or unread messages."

        briefing_items = []
        for c in unread:
            msg_str = f"Message: '{c['message']}'" if c['message'] != "No message left." else "No message left."
            briefing_items.append(f"• Missed call from {c['caller']} at {c['time']}. {msg_str}")
            c["briefed"] = True

        self._save()
        summary = "\n".join(briefing_items)
        full_text = f"Welcome back! While you were away, you missed {len(unread)} call(s):\n{summary}"
        return full_text

call_assistant = CallAssistantManager()

class RecordMissedCallTool(BaseTool):
    name = "record_missed_call"
    description = "Record a missed call and caller's text/voice message."
    parameters_schema = {
        "type": "object",
        "properties": {
            "caller": {"type": "string", "description": "Caller name or phone number"},
            "message": {"type": "string", "description": "Message content left by caller"}
        },
        "required": ["caller"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, caller: str, message: str = "", **kwargs) -> ToolResult:
        res = call_assistant.record_missed_call(caller, message)
        return ToolResult(True, res)

class CheckMissedCallsTool(BaseTool):
    name = "check_missed_calls"
    description = "Brief the user on missed calls and caller messages when available."
    parameters_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, **kwargs) -> ToolResult:
        briefing = call_assistant.get_unread_briefing()
        return ToolResult(True, briefing)

tool_registry.register(RecordMissedCallTool())
tool_registry.register(CheckMissedCallsTool())
