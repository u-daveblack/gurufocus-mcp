# GuruFocus MCP - JMESPath Query Feature Test

Test the JMESPath query functionality across various GuruFocus MCP tools. Run each test and verify the query correctly filters/transforms the data.

## Setup
Make sure the GuruFocus MCP server is configured in Claude Desktop with a valid API token.

---

## Schema Discovery Tests (Run First)

These tools help you understand the data structure before writing queries.

### List All Available Schemas
```
Call the list_schemas tool
```
Expected: Returns list of all available data models with categories.

### Get Specific Schema
```
Call get_schema with model_name "FinancialStatements"
```
Expected: Returns JSON schema for FinancialStatements model showing:
- `periods` array containing financial data
- Fields like `revenue`, `net_income`, `period`, etc.

### Get Category Schemas
```
Call get_schemas_by_category with category "stock_fundamentals"
```
Expected: Returns all schemas in the stock_fundamentals category (StockSummary, FinancialStatements, KeyRatios, etc.).

---

## Test Cases

### 1. Stock Financials - Recent Periods Only
Get Apple's financial statements but only the last 3 periods:
```
Call get_stock_financials for AAPL with period_type "annual" and query "periods[:3]"
```
Expected: Returns only 3 most recent annual periods.

### 2. Stock Financials - Revenue Trend
Extract just revenue figures from Apple's financials:
```
Call get_stock_financials for AAPL with query "periods[*].{period: period, revenue: revenue}"
```
Expected: Returns array of objects with just period and revenue fields.

### 3. Key Ratios - Profitability Focus
Get only profitability-related ratios for Microsoft:
```
Call get_stock_keyratios for MSFT with query "profitability"
```
Expected: Returns just the profitability object with roe, roa, roic, margins, etc.

### 4. Key Ratios - Valuation Metrics
Extract valuation metrics for Tesla:
```
Call get_stock_keyratios for TSLA with query "valuation"
```
Expected: Returns valuation object with pe_ratio, pb_ratio, ps_ratio, ev_to_ebitda, etc.

### 5. OHLC - Recent Price Data
Get the last 5 trading days for Google:
```
Call get_stock_price_ohlc for GOOG with query "bars[-5:]"
```
Expected: Returns only the 5 most recent price bars.

### 6. OHLC - Close Prices Only
Extract just dates and close prices from Amazon's price history:
```
Call get_stock_price_ohlc for AMZN with query "bars[*].{date: date, close: close}"
```
Expected: Returns array with just date and close for each bar.

### 7. Dividend History - Recent Dividends
Get the last 4 dividend payments for Johnson & Johnson:
```
Call get_stock_dividend for JNJ with query "payments[-4:]"
```
Expected: Returns only the 4 most recent dividend payments.

### 8. Stock Summary - Key Quality Scores
Get focused quality metrics for Nvidia:
```
Call get_stock_summary for NVDA with query "quality"
```
Expected: Returns quality object with gf_score, financial_strength, profitability_rank, etc.

### 9. Guru List - Top Gurus by Equity
Get guru list and filter to those with significant assets:
```
Call get_gurulist with query "gurus[:20]"
```
Expected: Returns first 20 gurus from the list.

### 10. Insider Updates - Recent Activity
Get recent insider updates:
```
Call get_insider_updates with query "updates[:10]"
```
Expected: Returns first 10 insider update transactions.

---

## Advanced Query Tests

### Nested Field Access
```
Call get_stock_keyratios for AAPL with query "{roe: profitability.roe, pe: valuation.pe_ratio, debt_equity: solvency.debt_to_equity}"
```
Expected: Returns flat object with selected nested fields.

### Filter with Condition
```
Call get_stock_price_ohlc for AAPL with start_date "20240101" and query "bars[?volume > `100000000`]"
```
Expected: Returns only bars where volume exceeded 100 million.

### Multiple Array Slices
```
Call get_stock_financials for MSFT with query "{recent: periods[:3], oldest: periods[-3:]}"
```
Expected: Returns object with both recent and oldest periods.

---

## Verification Checklist

For each test, verify:
- [ ] The query executes without errors
- [ ] The returned data is filtered/transformed as expected
- [ ] Both TOON and JSON formats work correctly with queries
- [ ] Invalid queries return helpful error messages

### Test Invalid Query Handling
```
Call get_stock_summary for AAPL with query "[[[invalid"
```
Expected: Should return an error message about invalid JMESPath syntax.

---

## Combined Format + Query Tests

### TOON Format with Query
```
Call get_stock_financials for AAPL with format "toon" and query "periods[:2]"
```
Expected: Query filters data first, then TOON encoding is applied to the result.

### JSON Format with Query
```
Call get_stock_financials for AAPL with format "json" and query "periods[:2]"
```
Expected: Query filters data, returns standard JSON.

---

## Tips for Writing Queries

1. **Always check the schema first**: Call `get_schema("ModelName")` to see available fields
2. **Use array slicing for pagination**: `periods[:5]` gets first 5, `periods[-5:]` gets last 5
3. **Project specific fields**: `periods[*].{a: field_a, b: field_b}` creates new objects
4. **Access nested data**: `profitability.roe` for nested fields
5. **Filter with conditions**: `[?field > \`value\`]` (note: backticks for literals)
