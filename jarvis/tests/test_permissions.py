"""
test_permissions.py - Pytest unit tests for 3-Tier Security Permissions
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.permissions import PermissionManager
from config.constants import PermissionLevel, ConfirmationMode
from config.settings import settings

def test_safe_tool_permission():
    settings.confirmation_mode = ConfirmationMode.BALANCED.value
    level, _ = PermissionManager.evaluate("open_application", {"app_name": "notepad"})
    assert level == PermissionLevel.SAFE

def test_confirm_tool_permission():
    settings.confirmation_mode = ConfirmationMode.BALANCED.value
    level, _ = PermissionManager.evaluate("send_whatsapp_message", {"recipient": "Rahul", "message": "Hi"})
    assert level == PermissionLevel.CONFIRM

def test_blocked_tool_permission():
    level, _ = PermissionManager.evaluate("bypass_auth_token", {})
    assert level == PermissionLevel.BLOCKED

def test_strict_mode_forces_confirmation():
    settings.confirmation_mode = ConfirmationMode.STRICT.value
    level, _ = PermissionManager.evaluate("open_application", {"app_name": "notepad"})
    assert level == PermissionLevel.CONFIRM
