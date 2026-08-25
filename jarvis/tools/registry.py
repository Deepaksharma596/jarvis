"""
registry.py - Dynamic Tool Registry for JARVIS
"""
import logging
from typing import Dict, List, Any, Optional
from tools.base_tool import BaseTool, ToolResult
from core.permissions import PermissionManager
from config.constants import PermissionLevel
from security.audit import AuditLogger

class ToolRegistry:
    """Discovers, validates, registers, and executes tools."""

    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        """Register a tool instance."""
        if tool.name in self._tools:
            logging.warning(f"[ToolRegistry] Overwriting tool registration for '{tool.name}'")
        self._tools[tool.name] = tool
        logging.info(f"[ToolRegistry] Registered tool: {tool.name}")

    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Retrieve registered tool by name."""
        return self._tools.get(name)

    def list_schemas(self) -> List[Dict[str, Any]]:
        """Return list of JSON schemas for all registered tools (for LLM function calling)."""
        schemas = []
        for name, tool in self._tools.items():
            schemas.append({
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters_schema
            })
        return schemas

    def execute_tool(self, name: str, user_command: str = "", mock: bool = False, **kwargs) -> ToolResult:
        """Find, permission check, execute, and verify a tool."""
        tool = self.get_tool(name)
        if not tool:
            res = ToolResult(success=False, output="", error=f"Tool '{name}' is not registered.")
            AuditLogger.log_action(user_command, name, kwargs, "", False, res.error)
            return res

        # Check permission level
        perm_level, reason = PermissionManager.evaluate(name, kwargs)

        if perm_level == PermissionLevel.BLOCKED:
            res = ToolResult(success=False, output="", error=f"Action blocked: {reason}")
            AuditLogger.log_action(user_command, name, kwargs, "", False, res.error)
            return res

        if mock:
            msg = f"[MOCK MODE] Would execute tool '{name}' with parameters {kwargs} ({reason})"
            logging.info(msg)
            res = ToolResult(success=True, output=msg, data={"mock": True})
            AuditLogger.log_action(user_command, name, kwargs, msg, True)
            return res

        try:
            logging.info(f"[ToolRegistry] Executing tool '{name}' with args {kwargs}")
            res = tool.execute(**kwargs)
            
            # Action verification check
            if res.success:
                verified = tool.verify(**kwargs)
                if not verified:
                    res.output += " (Note: Action completed but verification check reported uncertain UI state)."
            
            AuditLogger.log_action(user_command, name, kwargs, res.output, res.success, res.error)
            return res
        except Exception as e:
            err_msg = f"Execution exception in tool '{name}': {str(e)}"
            logging.error(f"[ToolRegistry] {err_msg}", exc_info=True)
            res = ToolResult(success=False, output="", error=err_msg)
            AuditLogger.log_action(user_command, name, kwargs, "", False, err_msg)
            return res

# Global Tool Registry Singleton
tool_registry = ToolRegistry()
