# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### gurufocus-api
- `stocks.get_quote()` - Real-time stock quote with OHLCV data and price changes
- `stocks.get_current_dividend()` - Current dividend yield, TTM dividends, and payment schedule
- `stocks.get_price_ohlc()` - Historical OHLC price bars with volume for technical analysis
- `stocks.get_volume()` - Historical trading volume data
- `stocks.get_unadjusted_price()` - Historical unadjusted (pre-split) prices
- New `InsidersEndpoint` class with 7 insider activity methods:
  - `insiders.get_updates()` - Recent insider transaction updates
  - `insiders.get_ceo_buys()` - CEO buy transactions
  - `insiders.get_cfo_buys()` - CFO buy transactions
  - `insiders.get_cluster_buys()` - Cluster buy signals (multiple insiders buying)
  - `insiders.get_double_buys()` - Double-down buy signals
  - `insiders.get_triple_buys()` - Triple-down buy signals
  - `insiders.get_list()` - List of known insiders

#### gurufocus-mcp
- `get_stock_quote` - MCP tool for real-time stock quotes
- `get_stock_dividend` - MCP tool for dividend history
- `get_stock_current_dividend` - MCP tool for current dividend information
- `get_stock_price_ohlc` - MCP tool for OHLC price history with date range support
- `get_stock_volume` - MCP tool for volume history with date range support
- `get_stock_unadjusted_price` - MCP tool for unadjusted price history
- 7 new insider activity tools:
  - `get_insider_updates` - Recent insider transactions
  - `get_insider_ceo_buys` - CEO buy transactions (bullish signal)
  - `get_insider_cfo_buys` - CFO buy transactions
  - `get_insider_cluster_buys` - Cluster buy signals
  - `get_insider_double_buys` - Double-down buy signals
  - `get_insider_triple_buys` - Triple-down buy signals
  - `get_insider_list` - Browse known insiders

## [v0.3.0] - 2025-12-27

### Added

#### gurufocus-api
- `stocks.get_trades_history()` - Guru trades history endpoint showing institutional buying/selling activity over time
- `stocks.get_gurus()` - Guru holdings and trading activity for a stock
- `stocks.get_executives()` - Company executives and directors

#### gurufocus-mcp
- `get_stock_trades_history` - MCP tool for guru trades history
- `get_stock_gurus` - MCP tool for guru holdings
- `get_stock_executives` - MCP tool for company executives

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
