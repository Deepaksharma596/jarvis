"""
whatsapp.py - WhatsApp Desktop & Web Automation Tools for JARVIS
"""
import time
import urllib.parse
import webbrowser
import logging
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from automation.windows import app_registry, WindowsAutomation
from automation.keyboard import KeyboardAutomation
from automation.mouse import MouseAutomation
from config.constants import PermissionLevel

class SendWhatsAppMessageTool(BaseTool):
    name = "send_whatsapp_message"
    description = "Send WhatsApp message to contact name or phone number."
    parameters_schema = {
        "type": "object",
        "properties": {
            "recipient": {"type": "string", "description": "Contact name or phone number with country code"},
            "message": {"type": "string", "description": "Message content text"}
        },
        "required": ["recipient", "message"]
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, recipient: str, message: str, **kwargs) -> ToolResult:
        encoded_msg = urllib.parse.quote(message)
        digits_only = "".join(filter(str.isdigit, recipient))

        # 1. Phone number direct send via whatsapp:// protocol
        if len(digits_only) >= 10:
            url = f"whatsapp://send?phone={digits_only}&text={encoded_msg}"
            try:
                webbrowser.open(url)
                time.sleep(2.5)
                KeyboardAutomation.press_key("enter")
                return ToolResult(True, f"Sent WhatsApp message to {recipient}: '{message}'")
            except Exception as e:
                logging.warning(f"[WhatsApp] Protocol launch failed: {e}")

        # 2. Launch WhatsApp app / protocol
        path = app_registry.find_app_path("whatsapp") or "whatsapp"
        WindowsAutomation.launch_app(path)
        time.sleep(2.0)

        # Focus search bar (Ctrl+F), search contact, type message & send
        KeyboardAutomation.hotkey("ctrl", "f")
        time.sleep(0.5)
        KeyboardAutomation.type_text(recipient)
        time.sleep(1.0)
        KeyboardAutomation.press_key("enter")
        time.sleep(0.5)
        KeyboardAutomation.type_text(message)
        time.sleep(0.5)
        KeyboardAutomation.press_key("enter")
        return ToolResult(True, f"Sent WhatsApp message to contact '{recipient}': '{message}'")

    def verify(self, recipient: str, message: str, **kwargs) -> bool:
        hwnds = WindowsAutomation.find_window_by_title("WhatsApp")
        return len(hwnds) > 0

class MakeWhatsAppCallTool(BaseTool):
    name = "make_whatsapp_call"
    description = "Start WhatsApp voice call with contact name."
    parameters_schema = {
        "type": "object",
        "properties": {
            "recipient": {"type": "string", "description": "Contact name to call"}
        },
        "required": ["recipient"]
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, recipient: str, **kwargs) -> ToolResult:
        path = app_registry.find_app_path("whatsapp") or "whatsapp"
        WindowsAutomation.launch_app(path)
        time.sleep(2.0)
        KeyboardAutomation.hotkey("ctrl", "f")
        time.sleep(0.5)
        KeyboardAutomation.type_text(recipient)
        time.sleep(1.0)
        KeyboardAutomation.press_key("enter")
        time.sleep(0.5)
        KeyboardAutomation.hotkey("ctrl", "shift", "c")
        return ToolResult(True, f"Initiated WhatsApp call to '{recipient}'.")

tool_registry.register(SendWhatsAppMessageTool())
tool_registry.register(MakeWhatsAppCallTool())
