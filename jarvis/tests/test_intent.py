"""
test_intent.py - Pytest unit tests for Intent Detection & Tool Parsing
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.agent import MockAIProvider, JARVISAgent
from config.settings import settings

def test_mock_intent_open_app():
    provider = MockAIProvider()
    tools = provider.select_tools("Open Brave", [])
    assert len(tools) == 1
    assert tools[0]["name"] == "open_application"
    assert tools[0]["kwargs"]["app_name"] == "brave"

def test_mock_intent_whatsapp():
    provider = MockAIProvider()
    tools = provider.select_tools("WhatsApp Rahul: I will reach at 7", [])
    assert len(tools) == 1
    assert tools[0]["name"] == "send_whatsapp_message"
    assert tools[0]["kwargs"]["recipient"] == "rahul"
    assert "7" in tools[0]["kwargs"]["message"]

def test_mock_intent_volume():
    provider = MockAIProvider()
    tools = provider.select_tools("Turn the volume down", [])
    assert len(tools) == 1
    assert tools[0]["name"] == "control_volume"
    assert tools[0]["kwargs"]["action"] == "down"
