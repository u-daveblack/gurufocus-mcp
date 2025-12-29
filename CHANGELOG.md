# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v0.5.1] - 2025-12-29

### Removed

#### gurufocus-mcp
- Removed `qgarp_scorecard` and `execution_risk_analysis` prompts from the MCP server to keep the server generic and allow users to apply their own investment methodologies

### Added

#### gurufocus-api
- `stocks.get_operating_data()` - Operating metrics and KPIs (revenue per employee, units shipped, etc.)
- `stocks.get_segments_data()` - Business and geographic segment revenue breakdown
- `stocks.get_ownership()` - Current ownership breakdown (institutional, insider, float)
- `stocks.get_indicator_history()` - Historical ownership indicator data
- `stocks.get_indicators()` - List of 240+ available stock indicators
- `stocks.get_indicator()` - Time series data for a specific indicator
- New `GurusEndpoint` class with 4 guru data methods:
  - `gurus.get_gurulist()` - List all tracked institutional gurus (~2.6MB dataset)
  - `gurus.get_guru_picks()` - Guru's stock picks with transaction details
  - `gurus.get_guru_aggregated()` - Guru's complete aggregated portfolio
  - `gurus.get_realtime_picks()` - Real-time guru trading activity across all investors
- New `PoliticiansEndpoint` class with 2 politician trading methods:
  - `politicians.get_politicians()` - List all tracked politicians (senators, representatives)
  - `politicians.get_transactions()` - Politician stock transactions with filters
- New `ReferenceEndpoint` class with 4 reference data methods:
  - `reference.get_exchange_list()` - List worldwide stock exchanges by country
  - `reference.get_exchange_stocks()` - Stocks listed on a specific exchange
  - `reference.get_index_list()` - List worldwide market indexes
  - `reference.get_index_stocks()` - Stocks in a market index (with pagination)
- New `EconomicEndpoint` class with 3 economic data methods:
  - `economic.get_indicators_list()` - List available economic indicators (GDP, CPI, unemployment, etc.)
  - `economic.get_indicator()` - Time series data for a specific economic indicator
  - `economic.get_calendar()` - Financial calendar events (earnings, dividends, IPOs, splits)

#### gurufocus-mcp
- `get_stock_operating_data` - MCP tool for operating metrics and business KPIs
- `get_stock_segments_data` - MCP tool for business and geographic segment analysis
- `get_stock_ownership` - MCP tool for ownership breakdown analysis
- `get_stock_indicator_history` - MCP tool for historical ownership trends
- `get_stock_indicators` - MCP tool to discover available indicators
- `get_stock_indicator` - MCP tool for specific indicator time series
- 4 new guru data tools:
  - `get_gurulist` - List all tracked super investors
  - `get_guru_picks` - Get a guru's stock picks and trading activity
  - `get_guru_aggregated` - Get a guru's complete portfolio with holdings
  - `get_guru_realtime_picks` - Recent trading activity across all gurus
- 2 new politician trading tools:
  - `get_politicians` - List all tracked politicians (senators, representatives)
  - `get_politician_transactions` - Politician stock transactions with filters
- 4 new reference data tools:
  - `get_exchange_list` - List worldwide stock exchanges by country
  - `get_exchange_stocks` - Stocks listed on a specific exchange
  - `get_index_list` - List worldwide market indexes (S&P 500, Dow 30, etc.)
  - `get_index_stocks` - Constituent stocks in a market index
- 3 new economic data tools:
  - `get_economic_indicators` - List available economic indicators
  - `get_economic_indicator` - Time series data for a specific indicator
  - `get_financial_calendar` - Financial calendar events (earnings, dividends, IPOs, splits)

## [v0.4.0] - 2025-12-28

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
