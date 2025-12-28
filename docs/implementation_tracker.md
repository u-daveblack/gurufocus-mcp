# GuruFocus Implementation Tracker

This document tracks implementation status across both packages:
- **gurufocus-api**: Python client library for the GuruFocus API
- **gurufocus-mcp**: MCP server exposing GuruFocus data to LLMs

## Progress Summary

| Package       | Implemented | Total | Progress |
| ------------- | ----------- | ----- | -------- |
| gurufocus-api | 22          | 52    | 42%      |
| gurufocus-mcp | 21          | 52    | 40%      |

---

## Analysis Tools (MCP Only)

These tools compute derived analysis from multiple GuruFocus endpoints:

| Tool                        | Description                                    | Status |
| --------------------------- | ---------------------------------------------- | ------ |
| `get_qgarp_analysis`        | QGARP investment screening scorecard           | ✅      |
| `get_stock_risk_analysis`   | Quantitative risk analysis (5 dimensions)      | ✅      |

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

| Endpoint                                | API | MCP | Notes                |
| --------------------------------------- | --- | --- | -------------------- |
| `GET /stock/{symbol}/indicator_history` | ❌   | ❌   | Historical ownership |
| `GET /stock/{symbol}/ownership`         | ❌   | ❌   | Current ownership    |

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

| Endpoint                               | API                                | MCP | Notes            |
| -------------------------------------- | ---------------------------------- | --- | ---------------- |
| `GET /stock/{symbol}/analyst_estimate` | ✅ `stocks.get_analyst_estimates()` | ❌   |                  |
| `GET /stock/{symbol}/estimate_history` | ❌                                  | ❌   | Forecast history |

### Operating & Segment Data

| Endpoint                             | API | MCP | Notes |
| ------------------------------------ | --- | --- | ----- |
| `GET /stock/{symbol}/operating_data` | ❌   | ❌   |       |
| `GET /stock/{symbol}/segments_data`  | ❌   | ❌   |       |

### Indicators

| Endpoint                              | API | MCP | Notes               |
| ------------------------------------- | --- | --- | ------------------- |
| `GET /stock/indicators`               | ❌   | ❌   | List all indicators |
| `GET /stock/{symbol}/{indicator_key}` | ❌   | ❌   | Specific indicator  |

### News

| Endpoint               | API | MCP | Notes           |
| ---------------------- | --- | --- | --------------- |
| `GET /stock/news_feed` | ❌   | ❌   | Stock headlines |

---

## Guru / Insider Data Endpoints

### Guru Data

| Endpoint                                   | API | MCP | Notes                                  |
| ------------------------------------------ | --- | --- | -------------------------------------- |
| `GET /gurulist`                            | ❌   | ❌   | All gurus                              |
| `GET /guru/{id}/picks/{start_date}/{page}` | ❌   | ❌   | Optional: `end_date`                   |
| `GET /guru/{id}/aggregated`                | ❌   | ❌   | Optional: `page`, `portdate`           |
| `GET /guru_realtime_picks`                 | ❌   | ❌   | Optional: `page`, `action`, `portdate` |

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

| Endpoint                        | API | MCP | Notes                                                 |
| ------------------------------- | --- | --- | ----------------------------------------------------- |
| `GET /politicians`              | ❌   | ❌   | Politician list                                       |
| `GET /politicians/transactions` | ❌   | ❌   | Optional: `page`, `asset_type`, `id`, `sort`, `order` |

---

## Economic Indicators Data Endpoints

| Endpoint                                   | API | MCP | Notes               |
| ------------------------------------------ | --- | --- | ------------------- |
| `GET /economicindicators`                  | ❌   | ❌   | List all indicators |
| `GET /economicindicators/item/{indicator}` | ❌   | ❌   | Specific indicator  |

---

## General Data Endpoints

### Exchange & Stock Lists

| Endpoint                               | API | MCP | Notes                |
| -------------------------------------- | --- | --- | -------------------- |
| `GET /exchange_list`                   | ❌   | ❌   | Worldwide exchanges  |
| `GET /exchange_stocks/{exchange_name}` | ❌   | ❌   | Stocks in exchange   |
| `GET /funda_updated/{date}`            | ❌   | ❌   | Updated fundamentals |

### Currency

| Endpoint                | API | MCP | Notes            |
| ----------------------- | --- | --- | ---------------- |
| `GET /country_currency` | ❌   | ❌   | Currency symbols |

### Index Data

| Endpoint                           | API | MCP | Notes             |
| ---------------------------------- | --- | --- | ----------------- |
| `GET /index_list`                  | ❌   | ❌   | Worldwide indexes |
| `GET /index_stocks/{index_symbol}` | ❌   | ❌   | Optional: `page`  |

### Financial Calendars

| Endpoint        | API | MCP | Notes                              |
| --------------- | --- | --- | ---------------------------------- |
| `GET /calendar` | ❌   | ❌   | Required: `date`; Optional: `type` |

---

## Personal Data Endpoints

### API Usage

| Endpoint         | API | MCP | Notes             |
| ---------------- | --- | --- | ----------------- |
| `GET /api_usage` | ❌   | ❌   | Usage information |

### User Portfolios (V2)

| Endpoint                               | API | MCP | Notes            |
| -------------------------------------- | --- | --- | ---------------- |
| `GET /v2/{api_token}/portfolios`       | ❌   | ❌   | List portfolios  |
| `POST /v2/{api_token}/portfolios/{id}` | ❌   | ❌   | Portfolio detail |

### User Screeners

| Endpoint                                   | API | MCP | Notes             |
| ------------------------------------------ | --- | --- | ----------------- |
| `GET /user_screeners`                      | ❌   | ❌   | List screeners    |
| `GET /user_screeners/{screener_id}/{page}` | ❌   | ❌   | Premium Plus only |

---

## ETF Data Endpoints

| Endpoint                          | API | MCP | Notes                        |
| --------------------------------- | --- | --- | ---------------------------- |
| `GET /etf/etf_list`               | ❌   | ❌   | Optional: `page`, `per_page` |
| `GET /etf/{ETF}/sector_weighting` | ❌   | ❌   | Sector weighting             |

---

## Implementation Summary by Category

| Category              | API       | MCP       | Total Endpoints |
| --------------------- | --------- | --------- | --------------- |
| Stock Summary & Basic | 4/4       | 4/4       | 4               |
| Price & Volume        | 4/4       | 3/4       | 4               |
| Ownership             | 0/2       | 0/2       | 2               |
| Trading Activity      | 4/4       | 3/4       | 4               |
| Dividend              | 2/2       | 2/2       | 2               |
| Estimates & Forecasts | 1/2       | 0/2       | 2               |
| Operating & Segment   | 0/2       | 0/2       | 2               |
| Indicators            | 0/2       | 0/2       | 2               |
| News                  | 0/1       | 0/1       | 1               |
| Guru Data             | 0/4       | 0/4       | 4               |
| Insider Data          | 7/7       | 7/7       | 7               |
| Politician Data       | 0/2       | 0/2       | 2               |
| Economic Indicators   | 0/2       | 0/2       | 2               |
| General Data          | 0/7       | 0/7       | 7               |
| Personal Data         | 0/5       | 0/5       | 5               |
| ETF Data              | 0/2       | 0/2       | 2               |
| **Total**             | **22/52** | **21/52** | **52**          |
