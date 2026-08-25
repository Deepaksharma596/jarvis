"""
desktop.py - Application Launcher & Desktop Control Tools for JARVIS
"""
import os
import time
from tools.base_tool import BaseTool, ToolResult
from tools.registry import tool_registry
from automation.windows import app_registry, WindowsAutomation
from automation.mouse import MouseAutomation
from automation.keyboard import KeyboardAutomation
from automation.screenshots import ScreenCapture
from config.constants import PermissionLevel

class OpenApplicationTool(BaseTool):
    name = "open_application"
    description = "Open desktop application by name (e.g. Brave, Chrome, WhatsApp, Notepad, VS Code)."
    parameters_schema = {
        "type": "object",
        "properties": {
            "app_name": {"type": "string", "description": "Name of app to launch"}
        },
        "required": ["app_name"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, app_name: str, **kwargs) -> ToolResult:
        path = app_registry.find_app_path(app_name)
        if path:
            success = WindowsAutomation.launch_app(path)
            if success:
                return ToolResult(True, f"Opened {app_name}.")
            return ToolResult(False, "", f"Failed to launch path '{path}' for '{app_name}'.")
        
        # Fallback to direct Windows startfile attempt
        success = WindowsAutomation.launch_app(app_name)
        if success:
            return ToolResult(True, f"Launched {app_name}.")
        return ToolResult(False, "", f"Application '{app_name}' not found in registry.")

    def verify(self, app_name: str, **kwargs) -> bool:
        time.sleep(1.0)
        hwnds = WindowsAutomation.find_window_by_title(app_name)
        return len(hwnds) > 0

class CloseApplicationTool(BaseTool):
    name = "close_application"
    description = "Close running desktop application window by name."
    parameters_schema = {
        "type": "object",
        "properties": {
            "app_name": {"type": "string", "description": "Name or title of application to close"}
        },
        "required": ["app_name"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, app_name: str, **kwargs) -> ToolResult:
        success = WindowsAutomation.close_window(app_name)
        if success:
            return ToolResult(True, f"Closed window for '{app_name}'.")
        return ToolResult(False, "", f"No active window found matching '{app_name}'.")

class SwitchWindowTool(BaseTool):
    name = "switch_window"
    description = "Switch focus to an open window."
    parameters_schema = {
        "type": "object",
        "properties": {
            "title": {"type": "string", "description": "Title substring of target window"}
        },
        "required": ["title"]
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, title: str, **kwargs) -> ToolResult:
        success = WindowsAutomation.focus_window(title)
        if success:
            return ToolResult(True, f"Switched to '{title}'.")
        return ToolResult(False, "", f"Could not find open window with title '{title}'.")

class TakeScreenshotTool(BaseTool):
    name = "take_screenshot"
    description = "Capture desktop screenshot."
    parameters_schema = {
        "type": "object",
        "properties": {},
        "required": []
    }
    default_permission_level = PermissionLevel.SAFE

    def execute(self, **kwargs) -> ToolResult:
        path = ScreenCapture.capture_to_file()
        if path:
            return ToolResult(True, f"Screenshot saved to {path}", data={"path": path})
        return ToolResult(False, "", "Failed to capture screenshot.")

class ClickScreenTool(BaseTool):
    name = "click_screen"
    description = "Click specified screen coordinates or current mouse location."
    parameters_schema = {
        "type": "object",
        "properties": {
            "x": {"type": "integer", "description": "X coordinate"},
            "y": {"type": "integer", "description": "Y coordinate"},
            "button": {"type": "string", "description": "left or right"},
            "clicks": {"type": "integer", "description": "Number of clicks"}
        },
        "required": []
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, x: int = None, y: int = None, button: str = "left", clicks: int = 1, **kwargs) -> ToolResult:
        MouseAutomation.click(x=x, y=y, button=button, clicks=clicks)
        return ToolResult(True, f"Clicked mouse at ({x}, {y})")

class TypeTextTool(BaseTool):
    name = "type_text"
    description = "Type text string using keyboard automation."
    parameters_schema = {
        "type": "object",
        "properties": {
            "text": {"type": "string", "description": "Text to type"}
        },
        "required": ["text"]
    }
    default_permission_level = PermissionLevel.CONFIRM

    def execute(self, text: str, **kwargs) -> ToolResult:
        KeyboardAutomation.type_text(text)
        return ToolResult(True, f"Typed text: '{text}'")

# Register desktop tools automatically
tool_registry.register(OpenApplicationTool())
tool_registry.register(CloseApplicationTool())
tool_registry.register(SwitchWindowTool())
tool_registry.register(TakeScreenshotTool())
tool_registry.register(ClickScreenTool())
tool_registry.register(TypeTextTool())
