"""
permissions.py - Permission and Safety Policy Manager for JARVIS
"""
from typing import Tuple
from config.constants import PermissionLevel, ConfirmationMode
from config.settings import settings

class PermissionManager:
    """Evaluates safety of tool execution requests based on confirmation mode and action tier."""

    # Default tool classification mappings
    SAFE_TOOLS = {
        "open_application", "close_application", "search_web", "open_url",
        "read_webpage", "get_system_info", "control_volume", "control_brightness",
        "take_screenshot", "open_file", "search_email", "read_email", "list_files",
        "read_pdf", "get_calendar", "get_battery_status"
    }

    CONFIRM_TOOLS = {
        "send_whatsapp_message", "make_whatsapp_call", "send_email",
        "create_email_draft", "delete_file", "move_file", "rename_file",
        "lock_computer", "shutdown_computer", "restart_computer",
        "click_screen", "type_text", "press_key", "hotkey"
    }

    BLOCKED_PATTERNS = [
        "steal_password", "bypass_auth", "format_drive", "install_malware",
        "export_credentials", "read_raw_sam"
    ]

    @classmethod
    def evaluate(cls, tool_name: str, params: dict) -> Tuple[PermissionLevel, str]:
        """
        Returns (PermissionLevel, Reason)
        """
        # 1. Check blocked patterns
        for pattern in cls.BLOCKED_PATTERNS:
            if pattern in tool_name.lower():
                return PermissionLevel.BLOCKED, f"Tool '{tool_name}' matches prohibited security pattern."

        mode = settings.confirmation_mode

        # 2. Strict Mode -> All external tools require confirmation except pure read-only system info
        if mode == ConfirmationMode.STRICT.value:
            if tool_name in {"get_system_info", "take_screenshot"}:
                return PermissionLevel.SAFE, "Read-only system check."
            return PermissionLevel.CONFIRM, f"Strict confirmation mode active for action '{tool_name}'."

        # 3. Trusted Mode -> Pre-approved actions or trusted recipients skip prompt
        if mode == ConfirmationMode.TRUSTED.value:
            if tool_name in cls.SAFE_TOOLS or tool_name in cls.CONFIRM_TOOLS:
                recipient = params.get("recipient", "").lower()
                if recipient and any(tc.lower() in recipient for tc in settings.trusted_contacts):
                    return PermissionLevel.SAFE, f"Recipient '{recipient}' is in trusted contacts."
                if tool_name not in {"delete_file", "shutdown_computer", "restart_computer"}:
                    return PermissionLevel.SAFE, f"Trusted execution mode enabled for '{tool_name}'."

        # 4. Balanced Mode (Default)
        if tool_name in cls.SAFE_TOOLS:
            return PermissionLevel.SAFE, f"Tool '{tool_name}' is classified as SAFE."

        if tool_name in cls.CONFIRM_TOOLS:
            return PermissionLevel.CONFIRM, f"Action '{tool_name}' involves external communication or system state change."

        # Fallback for unclassified tools: require confirmation
        return PermissionLevel.CONFIRM, f"Unclassified tool '{tool_name}' defaults to user confirmation."
