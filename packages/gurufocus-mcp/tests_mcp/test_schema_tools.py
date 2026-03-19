"""Tests for schema discovery tools."""

import pytest

from gurufocus_mcp.config import MCPServerSettings
from gurufocus_mcp.server import create_server


@pytest.fixture
def server(monkeypatch: pytest.MonkeyPatch):
    """Create a test server."""
    monkeypatch.setenv("GURUFOCUS_API_TOKEN", "test-token")
    settings = MCPServerSettings(api_token="test-token")
    return create_server(settings)


class TestSchemaToolRegistration:
    """Tests for schema tool registration."""

    @pytest.mark.asyncio
    async def test_list_schemas_tool_registered(self, server) -> None:
        """Test that list_schemas tool is registered."""
        tools = await server.list_tools()
        tool_names = [t.name for t in tools]
        assert "list_schemas" in tool_names

    @pytest.mark.asyncio
    async def test_get_schema_tool_registered(self, server) -> None:
        """Test that get_schema tool is registered."""
        tools = await server.list_tools()
        tool_names = [t.name for t in tools]
        assert "get_schema" in tool_names

    @pytest.mark.asyncio
    async def test_get_schemas_by_category_tool_registered(self, server) -> None:
        """Test that get_schemas_by_category tool is registered."""
        tools = await server.list_tools()
        tool_names = [t.name for t in tools]
        assert "get_schemas_by_category" in tool_names

    @pytest.mark.asyncio
    async def test_list_schemas_has_description(self, server) -> None:
        """Test that list_schemas tool has a description."""
        tool = await server.get_tool("list_schemas")

        assert tool is not None
        assert tool.description is not None
        assert "schema" in tool.description.lower()

    @pytest.mark.asyncio
    async def test_get_schema_has_model_name_parameter(self, server) -> None:
        """Test that get_schema tool has model_name parameter."""
        tool = await server.get_tool("get_schema")

        assert tool is not None
        assert tool.parameters is not None
        # Check that model_name is in the schema
        schema = tool.parameters
        assert "model_name" in str(schema)

    @pytest.mark.asyncio
    async def test_get_schemas_by_category_has_category_parameter(self, server) -> None:
        """Test that get_schemas_by_category tool has category parameter."""
        tool = await server.get_tool("get_schemas_by_category")

        assert tool is not None
        assert tool.parameters is not None
        schema = tool.parameters
        assert "category" in str(schema)

    @pytest.mark.asyncio
    async def test_tool_count_includes_schema_tools(self, server) -> None:
        """Test that tool count includes the 3 schema tools (54 total)."""
        tools = await server.list_tools()
        # Should now be 54 (51 original + 3 schema tools)
        assert len(tools) == 54
