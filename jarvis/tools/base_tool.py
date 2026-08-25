"""
base_tool.py - Abstract Base Tool Interface
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from config.constants import PermissionLevel

class ToolResult:
    """Standardized tool execution result."""
    def __init__(self, success: bool, output: str, error: str = None, data: Any = None):
        self.success = success
        self.output = output
        self.error = error
        self.data = data

    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "data": self.data
        }

    def __repr__(self):
        return f"ToolResult(success={self.success}, output='{self.output[:100]}...', error={self.error})"

class BaseTool(ABC):
    """Base class for all tools executable by JARVIS."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool identifier name."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human & LLM readable description of tool function."""
        pass

    @property
    @abstractmethod
    def parameters_schema(self) -> Dict[str, Any]:
        """JSON Schema format for tool input parameters."""
        pass

    @property
    def default_permission_level(self) -> PermissionLevel:
        """Default safety classification level."""
        return PermissionLevel.SAFE

    @abstractmethod
    def execute(self, **kwargs) -> ToolResult:
        """Execute the tool action with validated parameters."""
        pass

    def verify(self, **kwargs) -> bool:
        """Verification step checking if the action actually took effect."""
        return True
