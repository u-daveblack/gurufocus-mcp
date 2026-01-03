"""File output utilities for large dataset handling.

When output_dir is configured, tools can write full data to files and return
file paths, allowing AI agents to write Python code that reads files directly
rather than consuming context window with large datasets.
"""

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from .config import get_settings


def get_output_dir() -> Path | None:
    """Get configured output directory, creating it if needed.

    Handles ~ expansion for home directory paths.

    Returns:
        Path to output directory, or None if disabled (empty string).
    """
    settings = get_settings()
    if not settings.output_dir or not settings.output_dir.strip():
        return None

    # Expand ~ to user's home directory
    output_dir = Path(settings.output_dir).expanduser()
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_data_file(
    data: BaseModel | dict[str, Any],
    category: str,
    filename: str,
) -> str | None:
    """Write data to a JSON file in the output directory.

    Args:
        data: Pydantic model or dict to write
        category: Subdirectory category (e.g., 'stocks', 'gurus')
        filename: Filename without extension (e.g., 'AAPL_financials_annual')

    Returns:
        Absolute file path as string, or None if output_dir not configured.
    """
    output_dir = get_output_dir()
    if output_dir is None:
        return None

    # Create category subdirectory
    category_dir = output_dir / category
    category_dir.mkdir(parents=True, exist_ok=True)

    # Write file
    file_path = category_dir / f"{filename}.json"

    if isinstance(data, BaseModel):
        content = data.model_dump_json(indent=2, exclude_none=True)
    else:
        content = json.dumps(data, indent=2, default=str)

    file_path.write_text(content)

    return str(file_path.absolute())


def build_file_response(
    data: BaseModel | dict[str, Any],
    category: str,
    filename: str,
    model_name: str,
    preview: list[dict[str, Any]] | dict[str, Any],
    summary: dict[str, Any],
) -> dict[str, Any]:
    """Build an MCP-spec-compliant response with ResourceLink.

    Returns a response containing:
    - summary: Key metadata about the data
    - preview: Sample of the data for immediate context
    - resource_link: MCP-compliant ResourceLink pointing to the full data file

    The resource_link follows the MCP specification (2025-06-18):
    https://modelcontextprotocol.io/specification/2025-06-18/server/tools#resource-links

    Args:
        data: Full data to write to file
        category: Subdirectory category (e.g., 'stocks')
        filename: Filename without extension
        model_name: Pydantic model name for schema reference
        preview: Preview data (sample records or summary dict)
        summary: Summary metadata dict

    Returns:
        Response dict with MCP-compliant resource_link
    """
    file_path = write_data_file(data, category, filename)

    if file_path is None:
        # output_dir not configured - should not happen if caller checks
        raise RuntimeError("output_dir not configured")

    # Build MCP-spec-compliant ResourceLink
    # See: https://modelcontextprotocol.io/specification/2025-06-18/server/tools#resource-links
    resource_link = {
        "type": "resource_link",
        "uri": f"file://{file_path}",
        "name": f"{filename}.json",
        "description": f"Full {model_name} data. Read schema at gurufocus://schemas/{model_name}",
        "mimeType": "application/json",
        "annotations": {
            "audience": ["assistant"],
            "priority": 0.8,
        },
    }

    return {
        "summary": summary,
        "preview": preview,
        "resource_link": resource_link,
        "schema_uri": f"gurufocus://schemas/{model_name}",
    }


def is_file_output_enabled() -> bool:
    """Check if file output mode is enabled.

    Returns:
        True if output_dir is configured.
    """
    settings = get_settings()
    return bool(settings.output_dir)
