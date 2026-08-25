"""
__init__.py - Automatic Tool Discovery & Registration Package Initializer
"""
from tools.registry import tool_registry
import tools.desktop
import tools.browser
import tools.whatsapp
import tools.gmail
import tools.files
import tools.system
import tools.calendar
import tools.web_search
import tools.call_assistant

__all__ = ["tool_registry"]
