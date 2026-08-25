"""
planner.py - Multi-Step Task Planner for JARVIS
"""
import json
import logging
from typing import List, Dict, Any, Optional

class TaskPlanStep:
    """Represents a single step in a multi-step execution plan."""
    def __init__(self, step_number: int, description: str, tool_name: str, tool_params: dict, permission_level: str = "SAFE"):
        self.step_number = step_number
        self.description = description
        self.tool_name = tool_name
        self.tool_params = tool_params
        self.permission_level = permission_level
        self.status = "pending"  # pending, in_progress, completed, failed

    def to_dict(self) -> dict:
        return {
            "step_number": self.step_number,
            "description": self.description,
            "tool_name": self.tool_name,
            "tool_params": self.tool_params,
            "permission_level": self.permission_level,
            "status": self.status
        }

class TaskPlan:
    """Represents a complete multi-step task execution plan."""
    def __init__(self, user_command: str, steps: List[TaskPlanStep]):
        self.user_command = user_command
        self.steps = steps

    def is_complete(self) -> bool:
        return all(s.status == "completed" for s in self.steps)

    def is_failed(self) -> bool:
        return any(s.status == "failed" for s in self.steps)

    def to_dict(self) -> dict:
        return {
            "user_command": self.user_command,
            "steps": [s.to_dict() for s in self.steps]
        }

class TaskPlanner:
    """Decomposes complex requests into sequential TaskPlanSteps."""

    @staticmethod
    def create_simple_plan(user_command: str, tool_name: str, tool_params: dict, description: str = "") -> TaskPlan:
        """Create a single-step plan for direct tool invocations."""
        desc = description if description else f"Execute {tool_name}"
        step = TaskPlanStep(1, desc, tool_name, tool_params)
        return TaskPlan(user_command, [step])

    @staticmethod
    def parse_plan_json(user_command: str, plan_data: list) -> TaskPlan:
        """Parse structured JSON plan from AI model."""
        steps = []
        for i, raw in enumerate(plan_data, 1):
            step = TaskPlanStep(
                step_number=i,
                description=raw.get("description", f"Step {i}"),
                tool_name=raw.get("tool_name", ""),
                tool_params=raw.get("tool_params", {})
            )
            steps.append(step)
        return TaskPlan(user_command, steps)
