#!/bin/bash
# Test script for GuruFocus API endpoints
# Run: source .env && bash scripts/test_endpoints.sh

set -e

if [ -z "$GURUFOCUS_API_TOKEN" ]; then
    echo "ERROR: GURUFOCUS_API_TOKEN not set. Run: source .env"
    exit 1
fi

BASE_URL="https://api.gurufocus.com/public/user/${GURUFOCUS_API_TOKEN}"
SYMBOL="AAPL"
OUTPUT_DIR="packages/gurufocus-api/.responses"

mkdir -p "$OUTPUT_DIR"

test_endpoint() {
    local name="$1"
    local path="$2"
    local output_file="$OUTPUT_DIR/${name}.json"

    echo "========================================"
    echo "Testing: $name"
    echo "URL: $path"
    echo "----------------------------------------"

    response=$(curl -sL "${BASE_URL}${path}")

    # Check if error
    if echo "$response" | grep -q '"error"'; then
        echo "STATUS: FAILED"
        echo "$response"
    else
        echo "STATUS: SUCCESS"
        echo "$response" > "$output_file"
        echo "$response" | head -c 1500
        echo ""
        echo "..."
        echo "(Full response saved to $output_file)"
    fi
    echo ""
}

echo "=========================================="
echo "GuruFocus API Endpoint Test"
echo "Symbol: $SYMBOL"
echo "=========================================="
echo ""

# Batch 2: Price & Volume (with date params)
echo "### BATCH 2: Price & Volume ###"
test_endpoint "price_with_dates" "/stock/${SYMBOL}/price?start_date=20251201&end_date=20251227"
test_endpoint "unadjusted_price" "/stock/${SYMBOL}/unadjusted_price?start_date=20251201&end_date=20251227"
test_endpoint "price_ohlc" "/stock/${SYMBOL}/price_ohlc?start_date=20251201&end_date=20251227"
test_endpoint "volume" "/stock/${SYMBOL}/volume?start_date=20251201&end_date=20251227"

# Batch 3: Insider Activity
echo "### BATCH 3: Insider Activity ###"
test_endpoint "insider_updates" "/insider_updates?page=1"
test_endpoint "insider_ceo_buys" "/insider_buys/insider_ceo?page=1"
test_endpoint "insider_cfo_buys" "/insider_buys/insider_cfo?page=1"
test_endpoint "insider_cluster_buy" "/insider_buys/insider_cluster_buy?page=1"
test_endpoint "insider_double" "/insider_buys/insider_double?page=1"
test_endpoint "insider_triple" "/insider_buys/insider_triple?page=1"
test_endpoint "insider_list" "/insider_list?page=1"

# Batch 4: Business Segment & Operating Data
echo "### BATCH 4: Business Segments ###"
test_endpoint "operating_data" "/stock/${SYMBOL}/operating_data"
test_endpoint "segments_data" "/stock/${SYMBOL}/segments_data"

# Batch 5: Ownership & Indicators
echo "### BATCH 5: Ownership & Indicators ###"
test_endpoint "ownership" "/stock/${SYMBOL}/ownership"
test_endpoint "indicator_history" "/stock/${SYMBOL}/indicator_history"
test_endpoint "stock_indicators" "/stock/indicators"
test_endpoint "indicator_net_income" "/stock/${SYMBOL}/net_income?type=a"

# Batch 6: Guru Data
echo "### BATCH 6: Guru Data ###"
test_endpoint "gurulist" "/gurulist"
test_endpoint "guru_picks" "/guru/7/picks/2024-01-01/1"
test_endpoint "guru_aggregated" "/guru/7/aggregated?page=1"
test_endpoint "guru_realtime_picks" "/guru_realtime_picks?page=1"

# Batch 7: Politician Data
echo "### BATCH 7: Politician Data ###"
test_endpoint "politicians" "/politicians"
test_endpoint "politician_transactions" "/politicians/transactions?page=1"

# Batch 8: Reference Data
echo "### BATCH 8: Reference Data ###"
test_endpoint "exchange_list" "/exchange_list"
test_endpoint "exchange_stocks" "/exchange_stocks/NYSE"
test_endpoint "index_list" "/index_list"
test_endpoint "index_stocks" "/index_stocks/SP500"

# Batch 9: Economic Data
echo "### BATCH 9: Economic Data ###"
test_endpoint "economicindicators" "/economicindicators"
test_endpoint "economicindicator_gdp" "/economicindicators/item/gdp"
test_endpoint "calendar" "/calendar?date=2025-12-27"

# Batch 10: News & Estimates
echo "### BATCH 10: News & Estimates ###"
test_endpoint "news_feed" "/stock/news_feed?symbol=${SYMBOL}"
test_endpoint "estimate_history" "/stock/${SYMBOL}/estimate_history"

# Batch 11: ETF Data
echo "### BATCH 11: ETF Data ###"
test_endpoint "etf_list" "/etf/etf_list?page=1"
test_endpoint "etf_sector_weighting" "/etf/SPY/sector_weighting"

# Batch 12: Personal Data
echo "### BATCH 12: Personal Data ###"
test_endpoint "api_usage" "/api_usage"
test_endpoint "user_screeners" "/user_screeners"

# Batch 13: Misc Reference
echo "### BATCH 13: Misc Reference ###"
test_endpoint "country_currency" "/country_currency"
test_endpoint "funda_updated" "/funda_updated/2025-12-27"

echo "=========================================="
echo "Test Complete!"
echo "Results saved to: $OUTPUT_DIR/"
echo "=========================================="
