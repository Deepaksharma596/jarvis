"""
audit.py - Action Audit Logging with Secret Redaction
"""
import os
import json
import re
import datetime
import logging

LOG_DIR = os.path.join(os.path.expanduser("~"), ".jarvis", "logs")
AUDIT_LOG_FILE = os.path.join(LOG_DIR, "audit.jsonl")

SECRET_PATTERNS = [
    r'AI_API_KEY=["\']?([^"\']+)["\']?',
    r'bearer\s+[A-Za-z0-9\-\._~\+\/]+=*',
    r'sk-[A-Za-z0-9]{20,}',
    r'AIzaSy[A-Za-z0-9\-_]{33}',
    r'password=["\']?([^"\']+)["\']?',
]

class AuditLogger:
    """Logs every action executed by JARVIS with secrets automatically sanitized."""

    @staticmethod
    def _sanitize(text: str) -> str:
        if not isinstance(text, str):
            text = str(text)
        sanitized = text
        for pat in SECRET_PATTERNS:
            sanitized = re.sub(pat, "[REDACTED_SECRET]", sanitized, flags=re.IGNORECASE)
        return sanitized

    @classmethod
    def log_action(cls, user_command: str, tool_name: str, tool_params: dict, result: str, success: bool = True, error: str = None):
        """Append an audit record to JSONL log."""
        os.makedirs(LOG_DIR, exist_ok=True)
        record = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_command": cls._sanitize(user_command),
            "tool": tool_name,
            "params": {k: cls._sanitize(str(v)) for k, v in tool_params.items()},
            "success": success,
            "result": cls._sanitize(result),
            "error": cls._sanitize(error) if error else None
        }
        try:
            with open(AUDIT_LOG_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps(record) + "\n")
        except Exception as e:
            logging.error(f"[AuditLogger] Failed to write audit log: {e}")

    @classmethod
    def get_logs(cls, limit: int = 50) -> list:
        """Retrieve recent audit records."""
        if not os.path.exists(AUDIT_LOG_FILE):
            return []
        try:
            with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return [json.loads(line) for line in lines[-limit:]]
        except Exception as e:
            logging.error(f"[AuditLogger] Failed to read audit log: {e}")
            return []

    @classmethod
    def clear_logs(cls):
        """Clear audit history."""
        if os.path.exists(AUDIT_LOG_FILE):
            try:
                os.remove(AUDIT_LOG_FILE)
            except Exception as e:
                logging.error(f"[AuditLogger] Failed to clear audit log: {e}")
