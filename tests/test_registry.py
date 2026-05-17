"""Tests for tool registry."""

from aws_plumber.tools.registry import Tool, ToolRegistry


def test_tool_creation():
    """Test Tool creation."""
    def dummy_handler():
        pass

    tool = Tool(
        name="Test Tool",
        description="Test tool description",
        handler=dummy_handler,
        category="Test"
    )
    assert tool.name == "Test Tool"
    assert tool.description == "Test tool description"
    assert tool.enabled is True


def test_tool_registry_register():
    """Test registering a tool."""
    registry = ToolRegistry()

    def dummy_handler():
        pass

    registry.register("Test", "Test tool", dummy_handler, "Test")
    tools = registry.get_tools()
    assert len(tools) == 1
    assert tools[0].name == "Test"


def test_tool_registry_get_by_name():
    """Test getting a tool by name."""
    registry = ToolRegistry()

    def dummy_handler():
        pass

    registry.register("Test", "Test tool", dummy_handler)
    tool = registry.get_tool_by_name("Test")
    assert tool is not None
    assert tool.name == "Test"


def test_tool_registry_disable():
    """Test disabling a tool."""
    registry = ToolRegistry()

    def dummy_handler():
        pass

    registry.register("Test", "Test tool", dummy_handler)
    registry.disable_tool("Test")
    enabled_tools = registry.get_tools(enabled_only=True)
    assert len(enabled_tools) == 0
