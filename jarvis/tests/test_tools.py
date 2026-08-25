"""
test_tools.py - Pytest unit tests for Tool Registry & Execution
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.registry import tool_registry
from config.settings import settings

def test_tool_registry_discovery():
    schemas = tool_registry.list_schemas()
    names = [s["name"] for s in schemas]
    assert "open_application" in names
    assert "send_whatsapp_message" in names
    assert "read_email" in names

def test_mock_tool_execution():
    settings.mock_mode = True
    res = tool_registry.execute_tool("open_application", user_command="Open notepad", mock=True, app_name="notepad")
    assert res.success is True
    assert "[MOCK MODE]" in res.output
