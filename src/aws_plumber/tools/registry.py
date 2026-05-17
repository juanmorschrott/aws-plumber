"""Tool registry system for managing available tools."""

from typing import Callable, Optional
from dataclasses import dataclass


@dataclass
class Tool:
    """Represents an available CLI tool."""

    name: str
    description: str
    handler: Callable
    category: str = "General"
    enabled: bool = True


class ToolRegistry:
    """Registry for managing available tools."""

    def __init__(self):
        """Initialize the tool registry."""
        self._tools: list[Tool] = []

    def register(self, name: str, description: str, handler: Callable, category: str = "General") -> None:
        """Register a new tool."""
        tool = Tool(name=name, description=description, handler=handler, category=category)
        self._tools.append(tool)

    def get_tools(self, enabled_only: bool = True) -> list[Tool]:
        """Get all registered tools, optionally filtered by enabled status."""
        if enabled_only:
            return [t for t in self._tools if t.enabled]
        return self._tools

    def get_tool_by_name(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        for tool in self._tools:
            if tool.name == name:
                return tool
        return None

    def disable_tool(self, name: str) -> None:
        """Disable a tool."""
        for tool in self._tools:
            if tool.name == name:
                tool.enabled = False

    def enable_tool(self, name: str) -> None:
        """Enable a tool."""
        for tool in self._tools:
            if tool.name == name:
                tool.enabled = True


# Global tool registry
_registry = ToolRegistry()


def get_registry() -> ToolRegistry:
    """Get the global tool registry."""
    return _registry
