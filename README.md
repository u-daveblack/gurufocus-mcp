# Unofficial GuruFocus MCP Server & Python API Library

> NOTE: This repo is currently a work in progress and is not yet ready for production use.

A comprehensive GuruFocus MCP server and Python API client library with Pydantic models for all responses.

## Packages

This monorepo contains two packages:

### [gurufocus-api](./packages/gurufocus-api)

A standalone Python client library for the GuruFocus API.

- Full API coverage with type hints
- Three-tier earnings-aware caching
- Rate limiting and retry logic
- Pydantic models for all responses
- Async-first design with `httpx`

### [gurufocus-mcp](./packages/gurufocus-mcp)

An MCP server exposing GuruFocus data to AI assistants.

- FastMCP framework with HTTP/SSE transport
- **50+ tools** for stocks, gurus, insiders, politicians, economic data, and more
- Resources for direct data access
- **TOON format support** for 30-60% token reduction in LLM contexts

## Quick Start

### Installation

```bash
# Install both packages
pip install gurufocus-api gurufocus-mcp
```

### Using the API Client

```python
from gurufocus_api import GuruFocusClient

async with GuruFocusClient() as client:
    summary = await client.get_summary("AAPL")
    print(summary.gf_score)
```

### Running the MCP Server

```bash
export GURUFOCUS_API_TOKEN=your-token
gurufocus-mcp
```

### Claude Desktop Integration

First, install the package:

```bash
pipx install gurufocus-mcp   # recommended for CLI tools
# or
pip install gurufocus-mcp
```

Then add to your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "gurufocus": {
      "command": "gurufocus-mcp",
      "env": {
        "GURUFOCUS_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

After adding the configuration, restart Claude Desktop. You should see the GuruFocus tools available in Claude's interface.

**Running from source (for development):**

```json
{
  "mcpServers": {
    "gurufocus": {
      "command": "uv",
      "args": ["run", "gurufocus-mcp"],
      "env": {
        "GURUFOCUS_API_TOKEN": "your-token-here"
      }
    }
  }
}
```

### Output Format (TOON)

The MCP server supports [TOON format](https://github.com/toon-format/toon-python) for token-efficient responses, achieving 30-60% reduction in token usage compared to JSON.

**Per-request format selection:**

All tools accept a `format` parameter:
- `"toon"` (default) - Token-efficient format optimized for LLM contexts
- `"json"` - Standard JSON format for debugging or compatibility

```python
# TOON format (default)
result = await client.call_tool("get_stock_summary", {"symbol": "AAPL"})

# JSON format
result = await client.call_tool("get_stock_summary", {"symbol": "AAPL", "format": "json"})
```

**Environment variable configuration:**

```bash
# Change the default output format (default: toon)
export GURUFOCUS_DEFAULT_OUTPUT_FORMAT=json
```

## Configuration

All settings can be configured via environment variables with the `GURUFOCUS_` prefix.

### Required

| Variable              | Description              |
| --------------------- | ------------------------ |
| `GURUFOCUS_API_TOKEN` | Your GuruFocus API token |

### Cache Settings

| Variable                  | Default                | Description                 |
| ------------------------- | ---------------------- | --------------------------- |
| `GURUFOCUS_CACHE_ENABLED` | `true`                 | Enable response caching     |
| `GURUFOCUS_CACHE_DIR`     | `.cache/gurufocus-mcp` | Directory for cache storage |

**Recommended:** Set an absolute path for `GURUFOCUS_CACHE_DIR` to ensure consistent caching across sessions:

```bash
export GURUFOCUS_CACHE_DIR="$HOME/.cache/gurufocus-mcp"
```

Or in Claude Desktop config:

```json
{
  "mcpServers": {
    "gurufocus": {
      "command": "gurufocus-mcp",
      "env": {
        "GURUFOCUS_API_TOKEN": "your-token-here",
        "GURUFOCUS_CACHE_DIR": "/Users/yourname/.cache/gurufocus-mcp"
      }
    }
  }
}
```

### Rate Limiting

| Variable                       | Default | Description                              |
| ------------------------------ | ------- | ---------------------------------------- |
| `GURUFOCUS_RATE_LIMIT_ENABLED` | `true`  | Enable rate limiting                     |
| `GURUFOCUS_RATE_LIMIT_RPM`     | `30.0`  | Maximum requests per minute              |
| `GURUFOCUS_RATE_LIMIT_DAILY`   | `0`     | Maximum requests per day (0 = unlimited) |

### API Settings

| Variable                    | Default                                 | Description                                |
| --------------------------- | --------------------------------------- | ------------------------------------------ |
| `GURUFOCUS_API_BASE_URL`    | `https://api.gurufocus.com/public/user` | API base URL                               |
| `GURUFOCUS_API_TIMEOUT`     | `30.0`                                  | Request timeout in seconds                 |
| `GURUFOCUS_API_MAX_RETRIES` | `3`                                     | Maximum retry attempts for failed requests |

### Output Format

| Variable                          | Default | Description                                        |
| --------------------------------- | ------- | -------------------------------------------------- |
| `GURUFOCUS_DEFAULT_OUTPUT_FORMAT` | `toon`  | Default format: `toon` (token-efficient) or `json` |

### Logging

| Variable               | Default   | Description                                                   |
| ---------------------- | --------- | ------------------------------------------------------------- |
| `GURUFOCUS_LOG_LEVEL`  | `INFO`    | Logging level: `DEBUG`, `INFO`, `WARNING`, `ERROR`            |
| `GURUFOCUS_LOG_FORMAT` | `console` | Log format: `console` (human-readable) or `json` (structured) |

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/yourorg/gurufocus-mcp.git
cd gurufocus-mcp

# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-packages

# Run tests
uv run pytest

# Run tests with coverage
uv run pytest --cov --cov-report=html --junitxml=junit.xml

# Run linting
uv run ruff check .
```

### Project Structure

```
gurufocus-mcp/
├── packages/
│   ├── gurufocus-api/     # Python API client
│   └── gurufocus-mcp/     # MCP server
├── docs/                  # Documentation
├── examples/              # Usage examples
└── pyproject.toml         # Workspace config
```

## Disclaimer

This project is an unofficial tool and is not affiliated with, endorsed by, or sponsored by **GuruFocus.com, LLC** or any of its subsidiaries.

- **Non-Affiliation**: This software is developed independently and does not represent the views or opinions of GuruFocus.
- **Trademarks**: "GuruFocus" and the GuruFocus logo are trademarks of GuruFocus.com, LLC.
- **Data Usage**: Users are responsible for ensuring their use of this tool complies with the GuruFocus [Terms of Use](https://www.gurufocus.com/term-of-use) and any applicable API usage agreements. This tool is provided "as is" and intended for educational and personal use.
- **No Warranty**: The authors of this software make no warranty as to the accuracy, completeness, or reliability of the data retrieved using this tool.
- **No Investment Advice**: The information provided by this tool is for informational and educational purposes only and does not constitute investment advice, financial advice, trading advice, or any other sort of advice. You should not treat any of the tool's content as such.
- **External Methodologies**: References to third-party investment strategies, books, authors, or personalities (e.g., Phil Town, Rule #1, Warren Buffett) are for educational purposes to demonstrate the application of published methodologies. This project is not affiliated with, endorsed by, or sponsored by any referenced individuals or entities. All trademarks belong to their respective owners.

## License

MIT
