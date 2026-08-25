"""
system.py - Windows System Control Tools for JARVIS
"""
import ctypes
import subprocess
import logging
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from core.context import SystemContext
from automation.keyboard import KeyboardAutomation
from config.constants import PermissionLevel

class ControlVolumeTool(BaseTool):
    name = "control_volume"
    description = "Adjust or mute system master volume."
    parameters_schema = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "description": "up, down, or mute"}
        },
        "required": ["action"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, action: str, **kwargs) -> ToolResult:
        act = action.lower().strip()
        if act == "up":
            for _ in range(5):
                KeyboardAutomation.press_key("volumeup")
            return ToolResult(True, "Increased volume.")
        elif act == "down":
            for _ in range(5):
                KeyboardAutomation.press_key("volumedown")
            return ToolResult(True, "Decreased volume.")
        elif act == "mute":
            KeyboardAutomation.press_key("volumemute")
            return ToolResult(True, "Toggled volume mute.")
        return ToolResult(False, "", f"Unknown volume action '{action}'.")

class ControlBrightnessTool(BaseTool):
    name = "control_brightness"
    description = "Adjust screen brightness percentage."
    parameters_schema = {
        "type": "object",
        "properties": {
            "level": {"type": "integer", "description": "Target brightness level 0 to 100"}
        },
        "required": ["level"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, level: int, **kwargs) -> ToolResult:
        try:
            import screen_brightness_control as sbc
            sbc.set_brightness(level)
            return ToolResult(True, f"Set brightness to {level}%.")
        except Exception as e:
            return ToolResult(False, "", f"Could not adjust brightness: {e}")

class LockComputerTool(BaseTool):
    name = "lock_computer"
    description = "Lock the user's computer workstation immediately."
    parameters_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, **kwargs) -> ToolResult:
        try:
            ctypes.windll.user32.LockWorkStation()
            return ToolResult(True, "Locked workstation.")
        except Exception as e:
            return ToolResult(False, "", f"Failed to lock workstation: {e}")

class GetSystemInfoTool(BaseTool):
    name = "get_system_info"
    description = "Get CPU, RAM, Battery, and active window status."
    parameters_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, **kwargs) -> ToolResult:
        info = SystemContext.get_full_context_prompt()
        return ToolResult(True, f"System Status:\n{info}")

class ShutdownComputerTool(BaseTool):
    name = "shutdown_computer"
    description = "Shutdown computer system (Requires User Confirmation!)."
    parameters_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, **kwargs) -> ToolResult:
        try:
            subprocess.run("shutdown /s /t 30", shell=True)
            return ToolResult(True, "Initiated system shutdown in 30 seconds.")
        except Exception as e:
            return ToolResult(False, "", f"Failed to initiate shutdown: {e}")

tool_registry.register(ControlVolumeTool())
tool_registry.register(ControlBrightnessTool())
tool_registry.register(LockComputerTool())
tool_registry.register(GetSystemInfoTool())
tool_registry.register(ShutdownComputerTool())
