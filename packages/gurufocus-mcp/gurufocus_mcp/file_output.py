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

    Returns:
        Path to output directory, or None if not configured.
    """
    settings = get_settings()
    if not settings.output_dir:
        return None

    output_dir = Path(settings.output_dir)
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
    """Build a response with file path and preview data.

    This is the standard response format when output_dir is configured:
    - summary: Key metadata about the data
    - preview: Sample of the data for context
    - file_path: Where the full data was written
    - schema: URI to fetch the JSON schema

    Args:
        data: Full data to write to file
        category: Subdirectory category (e.g., 'stocks')
        filename: Filename without extension
        model_name: Pydantic model name for schema reference
        preview: Preview data (sample records or summary dict)
        summary: Summary metadata dict

    Returns:
        Response dict with file_path and preview
    """
    file_path = write_data_file(data, category, filename)

    if file_path is None:
        # output_dir not configured - should not happen if caller checks
        raise RuntimeError("output_dir not configured")

    return {
        "summary": summary,
        "preview": preview,
        "file_path": file_path,
        "schema": f"gurufocus://schemas/{model_name}",
        "python_hint": f"import pandas as pd; df = pd.read_json('{file_path}')",
    }


def is_file_output_enabled() -> bool:
    """Check if file output mode is enabled.

    Returns:
        True if output_dir is configured.
    """
    settings = get_settings()
    return bool(settings.output_dir)
