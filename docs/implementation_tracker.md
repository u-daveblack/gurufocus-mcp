# GuruFocus Implementation Tracker

This document tracks implementation status across both packages:
- **gurufocus-api**: Python client library for the GuruFocus API
- **gurufocus-mcp**: MCP server exposing GuruFocus data to LLMs

## Progress Summary

| Package       | Implemented | Total | Progress |
| ------------- | ----------- | ----- | -------- |
| gurufocus-api | 52          | 52    | 100%     |
| gurufocus-mcp | 53          | 52    | 100%     |

Note: MCP has 53 tools (50 endpoint wrappers + 3 analysis/utility tools)

---

## Analysis Tools (MCP Only)

These tools compute derived analysis from multiple GuruFocus endpoints:

| Tool                        | Description                                         | Status |
| --------------------------- | --------------------------------------------------- | ------ |
| `get_qgarp_analysis`        | QGARP investment screening scorecard                | ✅      |
| `get_stock_risk_analysis`   | Quantitative risk analysis (5 dimensions)           | ✅      |
| `get_usage_estimate`        | Estimate remaining API calls without using quota    | ✅      |

---

## Stock Data Endpoints

### Stock Summary & Basic Data

| Endpoint                         | API                         | MCP                       | Notes                     |
| -------------------------------- | --------------------------- | ------------------------- | ------------------------- |
| `GET /stock/{symbol}/summary`    | ✅ `stocks.get_summary()`    | ✅ `get_stock_summary`     |                           |
| `GET /stock/{symbol}/financials` | ✅ `stocks.get_financials()` | ✅ `get_stock_financials`  | Supports annual/quarterly |
| `GET /stock/{symbol}/keyratios`  | ✅ `stocks.get_keyratios()`  | ✅ `get_stock_keyratios`   |                           |
| `GET /stock/{symbol}/quote`      | ✅ `stocks.get_quote()`      | ✅ `get_stock_quote`        | Real-time quote data      |

### Price & Volume Data

| Endpoint                               | API                                 | MCP                             | Notes                        |
| -------------------------------------- | ----------------------------------- | ------------------------------- | ---------------------------- |
| `GET /stock/{symbol}/price`            | ✅ `stocks.get_price_history()`      | ❌                               | Supports start_date/end_date |
| `GET /stock/{symbol}/unadjusted_price` | ✅ `stocks.get_unadjusted_price()`   | ✅ `get_stock_unadjusted_price`  | Supports start_date/end_date |
| `GET /stock/{symbol}/price_ohlc`       | ✅ `stocks.get_price_ohlc()`         | ✅ `get_stock_price_ohlc`        | Full OHLC + volume           |
| `GET /stock/{symbol}/volume`           | ✅ `stocks.get_volume()`             | ✅ `get_stock_volume`            | Supports start_date/end_date |

### Ownership Data

| Endpoint                                | API                                | MCP                               | Notes                |
| --------------------------------------- | ---------------------------------- | --------------------------------- | -------------------- |
| `GET /stock/{symbol}/indicator_history` | ✅ `stocks.get_indicator_history()` | ✅ `get_stock_indicator_history`   | Historical ownership |
| `GET /stock/{symbol}/ownership`         | ✅ `stocks.get_ownership()`         | ✅ `get_stock_ownership`           | Current ownership    |

### Trading Activity

| Endpoint                             | API                              | MCP                            | Notes                 |
| ------------------------------------ | -------------------------------- | ------------------------------ | --------------------- |
| `GET /stock/{symbol}/gurus`          | ✅ `stocks.get_gurus()`           | ✅ `get_stock_gurus`            | Guru holdings & picks |
| `GET /stock/{symbol}/insider`        | ✅ `stocks.get_insider_trades()`  | ❌                              |                       |
| `GET /stock/{symbol}/executives`     | ✅ `stocks.get_executives()`      | ✅ `get_stock_executives`       | Company executives    |
| `GET /stock/{symbol}/trades/history` | ✅ `stocks.get_trades_history()`  | ✅ `get_stock_trades_history`   | Guru trades history   |

### Dividend Data

| Endpoint                               | API                                 | MCP                               | Notes                   |
| -------------------------------------- | ----------------------------------- | --------------------------------- | ----------------------- |
| `GET /stock/{symbol}/dividend`         | ✅ `stocks.get_dividends()`          | ✅ `get_stock_dividend`            | Dividend history        |
| `GET /stock/{symbol}/current_dividend` | ✅ `stocks.get_current_dividend()`   | ✅ `get_stock_current_dividend`    | Current yield & TTM div |

### Estimates & Forecasts

| Endpoint                               | API                                 | MCP                               | Notes            |
| -------------------------------------- | ----------------------------------- | --------------------------------- | ---------------- |
| `GET /stock/{symbol}/analyst_estimate` | ✅ `stocks.get_analyst_estimates()`  | ✅ `get_stock_analyst_estimates`   |                  |
| `GET /stock/{symbol}/estimate_history` | ✅ `stocks.get_estimate_history()`   | ✅ `get_stock_estimate_history`    | Forecast history |

### Operating & Segment Data

| Endpoint                             | API                               | MCP                            | Notes                          |
| ------------------------------------ | --------------------------------- | ------------------------------ | ------------------------------ |
| `GET /stock/{symbol}/operating_data` | ✅ `stocks.get_operating_data()`   | ✅ `get_stock_operating_data`   | Business operating metrics/KPIs |
| `GET /stock/{symbol}/segments_data`  | ✅ `stocks.get_segments_data()`    | ✅ `get_stock_segments_data`    | Business & geographic segments |

### Indicators

| Endpoint                              | API                           | MCP                      | Notes               |
| ------------------------------------- | ----------------------------- | ------------------------ | ------------------- |
| `GET /stock/indicators`               | ✅ `stocks.get_indicators()`   | ✅ `get_stock_indicators` | List all indicators |
| `GET /stock/{symbol}/{indicator_key}` | ✅ `stocks.get_indicator()`    | ✅ `get_stock_indicator`  | Specific indicator  |

### News

| Endpoint               | API                          | MCP                      | Notes                          |
| ---------------------- | ---------------------------- | ------------------------ | ------------------------------ |
| `GET /stock/news_feed` | ✅ `stocks.get_news_feed()`   | ✅ `get_stock_news_feed`  | Optional symbol filter support |

---

## Guru / Insider Data Endpoints

### Guru Data

| Endpoint                                   | API                              | MCP                         | Notes                                  |
| ------------------------------------------ | -------------------------------- | --------------------------- | -------------------------------------- |
| `GET /gurulist`                            | ✅ `gurus.get_gurulist()`         | ✅ `get_gurulist`            | All gurus (~2.6MB)                     |
| `GET /guru/{id}/picks/{start_date}/{page}` | ✅ `gurus.get_guru_picks()`       | ✅ `get_guru_picks`          | Optional: `start_date`, `page`         |
| `GET /guru/{id}/aggregated`                | ✅ `gurus.get_guru_aggregated()`  | ✅ `get_guru_aggregated`     | Full portfolio with holdings           |
| `GET /guru_realtime_picks`                 | ✅ `gurus.get_realtime_picks()`   | ✅ `get_guru_realtime_picks` | Optional: `page`                       |

### Insider Data

| Endpoint                                | API                               | MCP                          | Notes                                                            |
| --------------------------------------- | --------------------------------- | ---------------------------- | ---------------------------------------------------------------- |
| `GET /insider_updates`                  | ✅ `insiders.get_updates()`        | ✅ `get_insider_updates`      | Optional: `page`, `date`, `region`, `file_date`, `sort`, `order` |
| `GET /insider_buys/insider_ceo`         | ✅ `insiders.get_ceo_buys()`       | ✅ `get_insider_ceo_buys`     | Optional: `page`, `within_days`                                  |
| `GET /insider_buys/insider_cfo`         | ✅ `insiders.get_cfo_buys()`       | ✅ `get_insider_cfo_buys`     | Optional: `page`, `within_days`                                  |
| `GET /insider_buys/insider_cluster_buy` | ✅ `insiders.get_cluster_buys()`   | ✅ `get_insider_cluster_buys` | Optional: `page`, `within_days`                                  |
| `GET /insider_buys/insider_double`      | ✅ `insiders.get_double_buys()`    | ✅ `get_insider_double_buys`  | Optional: `page`, `within_days`                                  |
| `GET /insider_buys/insider_triple`      | ✅ `insiders.get_triple_buys()`    | ✅ `get_insider_triple_buys`  | Optional: `page`, `within_days`                                  |
| `GET /insider_list`                     | ✅ `insiders.get_list()`           | ✅ `get_insider_list`         | Optional: `page`                                                 |

### Politician Data

| Endpoint                        | API                                    | MCP                              | Notes                                                 |
| ------------------------------- | -------------------------------------- | -------------------------------- | ----------------------------------------------------- |
| `GET /politicians`              | ✅ `politicians.get_politicians()`      | ✅ `get_politicians`              | Politician list                                       |
| `GET /politicians/transactions` | ✅ `politicians.get_transactions()`     | ✅ `get_politician_transactions`  | Optional: `page`, `asset_type`, `id`, `sort`, `order` |

---

## Economic Indicators Data Endpoints

| Endpoint                                   | API                                    | MCP                          | Notes               |
| ------------------------------------------ | -------------------------------------- | ---------------------------- | ------------------- |
| `GET /economicindicators`                  | ✅ `economic.get_indicators_list()`     | ✅ `get_economic_indicators`  | List all indicators |
| `GET /economicindicators/item/{indicator}` | ✅ `economic.get_indicator()`           | ✅ `get_economic_indicator`   | Specific indicator  |

---

## General Data Endpoints

### Exchange & Stock Lists

| Endpoint                               | API                                  | MCP                     | Notes                |
| -------------------------------------- | ------------------------------------ | ----------------------- | -------------------- |
| `GET /exchange_list`                   | ✅ `reference.get_exchange_list()`    | ✅ `get_exchange_list`   | Worldwide exchanges  |
| `GET /exchange_stocks/{exchange_name}` | ✅ `reference.get_exchange_stocks()`  | ✅ `get_exchange_stocks` | Stocks in exchange   |
| `GET /funda_updated/{date}`            | ✅ `reference.get_funda_updated()`    | ✅ `get_funda_updated`   | Updated fundamentals |

### Currency

| Endpoint                | API                                   | MCP                      | Notes            |
| ----------------------- | ------------------------------------- | ------------------------ | ---------------- |
| `GET /country_currency` | ✅ `reference.get_country_currency()`  | ✅ `get_country_currency` | Currency symbols |

### Index Data

| Endpoint                           | API                                | MCP                   | Notes             |
| ---------------------------------- | ---------------------------------- | --------------------- | ----------------- |
| `GET /index_list`                  | ✅ `reference.get_index_list()`     | ✅ `get_index_list`    | Worldwide indexes |
| `GET /index_stocks/{index_symbol}` | ✅ `reference.get_index_stocks()`   | ✅ `get_index_stocks`  | Optional: `page`  |

### Financial Calendars

| Endpoint        | API                           | MCP                          | Notes                              |
| --------------- | ----------------------------- | ---------------------------- | ---------------------------------- |
| `GET /calendar` | ✅ `economic.get_calendar()`   | ✅ `get_financial_calendar`   | Required: `date`; Optional: `type` |

---

## Personal Data Endpoints

### API Usage

| Endpoint         | API                            | MCP                  | Notes             |
| ---------------- | ------------------------------ | -------------------- | ----------------- |
| `GET /api_usage` | ✅ `personal.get_api_usage()`   | ✅ `get_api_usage`    | Usage information |

### User Portfolios (V2)

| Endpoint                               | API                                  | MCP                     | Notes            |
| -------------------------------------- | ------------------------------------ | ----------------------- | ---------------- |
| `GET /v2/{api_token}/portfolios`       | ✅ `personal.get_portfolios()`        | ✅ `get_portfolios`      | List portfolios  |
| `POST /v2/{api_token}/portfolios/{id}` | ✅ `personal.get_portfolio_detail()`  | ✅ `get_portfolio_detail`| Portfolio detail |

### User Screeners

| Endpoint                                   | API                                       | MCP                            | Notes             |
| ------------------------------------------ | ----------------------------------------- | ------------------------------ | ----------------- |
| `GET /user_screeners`                      | ✅ `personal.get_user_screeners()`         | ✅ `get_user_screeners`         | List screeners    |
| `GET /user_screeners/{screener_id}/{page}` | ✅ `personal.get_user_screener_results()`  | ✅ `get_user_screener_results`  | Premium Plus only |

---

## ETF Data Endpoints

| Endpoint                          | API                       | MCP                | Notes                        |
| --------------------------------- | ------------------------- | ------------------ | ---------------------------- |
| `GET /etf/etf_list`               | ✅ `etfs.get_etf_list()`   | ✅ `get_etf_list`   | Optional: `page`, `per_page` |
| `GET /etf/{ETF}/sector_weighting` | ✅ `etfs.get_sector_weighting()` | ✅ `get_etf_sector_weighting` | Sector & industry weightings |

---

## Implementation Summary by Category

| Category              | API       | MCP       | Total Endpoints |
| --------------------- | --------- | --------- | --------------- |
| Stock Summary & Basic | 4/4       | 4/4       | 4               |
| Price & Volume        | 4/4       | 3/4       | 4               |
| Ownership             | 2/2       | 2/2       | 2               |
| Trading Activity      | 4/4       | 3/4       | 4               |
| Dividend              | 2/2       | 2/2       | 2               |
| Estimates & Forecasts | 2/2       | 2/2       | 2               |
| Operating & Segment   | 2/2       | 2/2       | 2               |
| Indicators            | 2/2       | 2/2       | 2               |
| News                  | 1/1       | 1/1       | 1               |
| Guru Data             | 4/4       | 4/4       | 4               |
| Insider Data          | 7/7       | 7/7       | 7               |
| Politician Data       | 2/2       | 2/2       | 2               |
| Economic Indicators   | 2/2       | 2/2       | 2               |
| Exchange & Index Data | 5/5       | 5/5       | 5               |
| Currency & Calendar   | 2/2       | 2/2       | 2               |
| Personal Data         | 5/5       | 5/5       | 5               |
| ETF Data              | 2/2       | 2/2       | 2               |
| **Total**             | **52/52** | **50/52** | **52**          |
