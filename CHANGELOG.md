# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-12-24

### Added

#### gurufocus-api
- Async Python client for GuruFocus API with `GuruFocusClient`
- Stock endpoints: summary, financials, keyratios, dividends, insiders, price, analyst estimates
- SQLite-backed disk cache with category-based TTLs
- Token bucket rate limiter with configurable daily limits
- Pydantic models for all API responses
- OpenTelemetry instrumentation support (optional)
- Retry logic with exponential backoff

#### gurufocus-mcp
- MCP server built on FastMCP
- Stock data tools: `get_stock_summary`, `get_stock_financials`, `get_stock_keyratios`, etc.
- QGARP (Quality, Growth, And Reasonable Price) analysis tool
- Risk analysis tool
- TOON format output for 30-60% token reduction vs JSON
- Stock resources with URI templates
- Structured prompts for stock analysis

[0.1.0]: https://github.com/u-daveblack/gurufocus-mcp/releases/tag/v0.1.0
