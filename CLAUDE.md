# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Development Commands

```bash
# Install dependencies (uses uv workspace)
uv sync --all-packages

# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov --cov-report=html --junitxml=junit.xml

# Run tests for a specific package
uv run pytest packages/gurufocus-api/tests/
uv run pytest packages/gurufocus-mcp/tests/

# Run a single test file or test
uv run pytest packages/gurufocus-api/tests/test_cache.py
uv run pytest packages/gurufocus-api/tests/test_cache.py::test_cache_hit

# Linting
uv run ruff check .
uv run ruff check . --fix  # auto-fix

# Type checking
uv run mypy packages/gurufocus-api/gurufocus_api packages/gurufocus-mcp/gurufocus_mcp

# Run the MCP server (requires GURUFOCUS_API_TOKEN)
export GURUFOCUS_API_TOKEN=your-token
uv run gurufocus-mcp
```

## Architecture

This is a **uv workspace monorepo** with two packages:

### `packages/gurufocus-api` (gurufocus_api)
Python async client for the GuruFocus API:
- **client.py**: Main `GuruFocusClient` class - async context manager with httpx, retry logic, OpenTelemetry support
- **endpoints/stocks.py**: `StocksEndpoint` with methods like `get_summary()` - uses Pydantic models
- **cache/**: Category-based caching system
  - `manager.py`: `CacheManager` with tier-aware TTLs per `CacheCategory`
  - `disk.py`: SQLite-backed `DiskCacheBackend`
- **models/**: Pydantic models for API responses (summary, financials, keyratios, etc.)
- **rate_limiter.py**: Token bucket rate limiting with daily limits

### `packages/gurufocus-mcp` (gurufocus_mcp)
MCP server built on FastMCP exposing GuruFocus data:
- **server.py**: `create_server()` factory with lifespan management, `main()` entry point
- **tools/stocks.py**: `register_stock_tools()` - MCP tools decorated with `@mcp.tool`
- **resources/stocks.py**: `register_stock_resources()` - MCP resources with URI templates
- **formatting.py**: TOON format support for 30-60% token reduction vs JSON

### Key Patterns
- API client uses lazy initialization: `client.stocks`, `client.cache`, `client.rate_limiter`
- MCP server stores shared `GuruFocusClient` in `mcp.state["client"]`
- All tools accept `format` parameter: `"toon"` (default) or `"json"`
- Pydantic models use `model_dump(mode="json", exclude_none=True)` for serialization

## Configuration

Environment variables (loaded via pydantic-settings):
- `GURUFOCUS_API_TOKEN`: Required API token
- `GURUFOCUS_DEFAULT_OUTPUT_FORMAT`: `toon` (default) or `json`
- Cache, rate limit, and logging settings in `gurufocus_api/config.py` and `gurufocus_mcp/config.py`

## Testing

Tests use `pytest-asyncio` with `asyncio_mode = "auto"`. API tests use `respx` to mock httpx requests. Test fixtures are in `packages/*/tests/conftest.py`.

## Changelog

When making changes, update `CHANGELOG.md` under the `[Unreleased]` section. Follow [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format with categories: Added, Changed, Deprecated, Removed, Fixed, Security.

## Readme

When adding or removing a feature always review the `README.md` in the root directory and the `README.md` in the `packages/gurufocus-api` and `packages/gurufocus-mcp` directories and update it if necessary.
