"""
test_call_assistant.py - Pytest unit tests for Missed Call & Availability Briefing
"""
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.call_assistant import call_assistant, RecordMissedCallTool, CheckMissedCallsTool
from core.agent import MockAIProvider

def test_record_and_brief_missed_call():
    # Clear test state
    call_assistant.missed_calls.clear()
    
    # Record a missed call
    rec_tool = RecordMissedCallTool()
    res = rec_tool.execute(caller="Rahul", message="Please call back when free.")
    assert res.success is True
    assert "Recorded missed call from Rahul" in res.output

    # Check unread briefing
    check_tool = CheckMissedCallsTool()
    res_brief = check_tool.execute()
    assert res_brief.success is True
    assert "Welcome back!" in res_brief.output
    assert "Missed call from Rahul" in res_brief.output
    assert "Please call back when free." in res_brief.output

def test_intent_parsing_missed_call():
    provider = MockAIProvider()
    tools = provider.select_tools("I'm back, check my missed calls", [])
    assert len(tools) == 1
    assert tools[0]["name"] == "check_missed_calls"
