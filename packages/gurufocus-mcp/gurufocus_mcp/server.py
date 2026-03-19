"""GuruFocus MCP Server.

This module implements the MCP server using FastMCP, exposing
GuruFocus financial data to AI assistants via the Model Context Protocol.
"""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastmcp import FastMCP

from gurufocus_api import GuruFocusClient
from gurufocus_api.logging import configure_logging, get_logger

from .config import MCPServerSettings, get_settings
from .resources import register_schema_resources, register_stock_resources
from .tools import (
    register_analysis_tools,
    register_economic_tools,
    register_etf_tools,
    register_guru_tools,
    register_insider_tools,
    register_personal_tools,
    register_politician_tools,
    register_reference_tools,
    register_schema_tools,
    register_stock_tools,
)

# Module-level state for the default server
_default_settings: MCPServerSettings | None = None


def create_server(settings: MCPServerSettings | None = None) -> FastMCP:
    """Create and configure the MCP server.

    Args:
        settings: Optional server settings. If not provided, loads from environment.

    Returns:
        Configured FastMCP server instance
    """
    global _default_settings

    if settings is None:
        settings = get_settings()

    _default_settings = settings

    # Configure structlog logging (aligned with gurufocus-api)
    configure_logging(
        log_level=settings.log_level,
        log_format=settings.log_format,
    )

    logger = get_logger(__name__)

    @asynccontextmanager
    async def lifespan(mcp: FastMCP) -> AsyncIterator[dict[str, Any]]:
        """Manage server lifecycle and shared resources."""
        if _default_settings is None or not _default_settings.validate_api_token():
            logger.warning("gurufocus_api_token_not_set")
            yield {"client": None}
            return

        # Create and share the GuruFocus client using async context manager
        # to ensure proper cleanup of SQLite cache connections
        async with GuruFocusClient(
            api_token=_default_settings.api_token,
            base_url=_default_settings.api_base_url,
            timeout=_default_settings.api_timeout,
            max_retries=_default_settings.api_max_retries,
            cache_enabled=_default_settings.cache_enabled,
            cache_dir=_default_settings.cache_dir,
            rate_limit_enabled=_default_settings.rate_limit_enabled,
            rate_limit_rpm=_default_settings.rate_limit_rpm,
            rate_limit_daily=_default_settings.rate_limit_daily,
        ) as client:
            logger.debug("gurufocus_client_initialized")
            tool_count = len(await mcp.list_tools())
            resource_count = len(await mcp.list_resources()) + len(
                await mcp.list_resource_templates()
            )
            logger.info(
                "gurufocus_mcp_server_created",
                resources=resource_count,
                tools=tool_count,
                server_name=_default_settings.server_name if _default_settings else "unknown",
                server_version=_default_settings.server_version if _default_settings else "unknown",
            )
            yield {"client": client}

    # Create the MCP server with lifespan
    mcp = FastMCP(
        name=settings.server_name,
        version=settings.server_version,
        lifespan=lifespan,
    )

    # Register tools and resources
    register_stock_tools(mcp)
    register_analysis_tools(mcp)
    register_insider_tools(mcp)
    register_guru_tools(mcp)
    register_politician_tools(mcp)
    register_reference_tools(mcp)
    register_economic_tools(mcp)
    register_etf_tools(mcp)
    register_personal_tools(mcp)
    register_schema_tools(mcp)
    register_stock_resources(mcp)
    register_schema_resources(mcp)

    return mcp


# Create the default server instance
mcp = create_server()


def main() -> None:
    """Entry point for the MCP server."""
    import sys

    # Check for API token
    settings = get_settings()

    # Configure logging before checking token
    configure_logging(
        log_level=settings.log_level,
        log_format=settings.log_format,
    )

    if not settings.validate_api_token():
        print(
            "Error: GURUFOCUS_API_TOKEN environment variable not set.\n"
            "Please set your GuruFocus API token:\n"
            "  export GURUFOCUS_API_TOKEN='your-api-token'",
            file=sys.stderr,
        )
        sys.exit(1)

    # Run the server
    mcp.run()


if __name__ == "__main__":
    main()
