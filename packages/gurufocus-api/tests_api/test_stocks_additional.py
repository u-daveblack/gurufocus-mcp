"""Tests for additional stock endpoints (estimates, dividends, price history, insider trades).

Note: Model parsing with real API responses is tested in test_models_with_fixtures.py.
These tests focus on endpoint behavior.
"""

import json
import tempfile
from pathlib import Path

import pytest
import respx
from httpx import Response

from gurufocus_api import (
    AnalystEstimates,
    DividendHistory,
    GuruFocusClient,
    InsiderTrades,
    PriceHistory,
)

# Load sample responses from fixtures
FIXTURES_DIR = Path(__file__).parent / "data"


def load_fixture(category: str, symbol: str = "FAKE1") -> dict | list:
    """Load a fixture file."""
    path = FIXTURES_DIR / category / f"{symbol}.json"
    with open(path) as f:
        return json.load(f)


SAMPLE_ESTIMATES_RESPONSE = load_fixture("analyst_estimate")
SAMPLE_DIVIDENDS_RESPONSE = load_fixture("dividend")
SAMPLE_PRICE_RESPONSE = load_fixture("price")
SAMPLE_INSIDERS_RESPONSE = load_fixture("insider")


class TestAnalystEstimatesEndpoint:
    """Tests for analyst estimates endpoint."""

    @pytest.fixture
    def cache_dir(self) -> Path:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_analyst_estimates(self, cache_dir: Path) -> None:
        """Test fetching analyst estimates returns typed model."""
        api_token = "test-token"
        respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/analyst_estimate"
        ).mock(return_value=Response(200, json=SAMPLE_ESTIMATES_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            estimates = await client.stocks.get_analyst_estimates("FAKE1")

            assert isinstance(estimates, AnalystEstimates)
            assert estimates.symbol == "FAKE1"
            # Annual estimates should be parsed from column-oriented data
            assert len(estimates.annual_estimates) > 0
            # First annual estimate should have revenue
            assert estimates.annual_estimates[0].revenue_estimate is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_analyst_estimates_cached(self, cache_dir: Path) -> None:
        """Test that estimates are cached."""
        api_token = "test-token"
        route = respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/analyst_estimate"
        ).mock(return_value=Response(200, json=SAMPLE_ESTIMATES_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            await client.stocks.get_analyst_estimates("FAKE1")
            await client.stocks.get_analyst_estimates("FAKE1")
            assert route.call_count == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_analyst_estimates_raw(self, cache_dir: Path) -> None:
        """Test fetching raw estimates data."""
        api_token = "test-token"
        respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/analyst_estimate"
        ).mock(return_value=Response(200, json=SAMPLE_ESTIMATES_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            raw = await client.stocks.get_analyst_estimates_raw("FAKE1")
            assert isinstance(raw, dict)
            # Real API returns annual/quarterly at top level
            assert "annual" in raw or "quarterly" in raw


class TestDividendsEndpoint:
    """Tests for dividends endpoint."""

    @pytest.fixture
    def cache_dir(self) -> Path:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_dividends(self, cache_dir: Path) -> None:
        """Test fetching dividends returns typed model."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/dividend").mock(
            return_value=Response(200, json=SAMPLE_DIVIDENDS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            dividends = await client.stocks.get_dividends("FAKE1")

            assert isinstance(dividends, DividendHistory)
            assert dividends.symbol == "FAKE1"
            # Real API returns array of dividend objects directly
            assert len(dividends.payments) > 0
            # First payment should have amount
            assert dividends.payments[0].amount is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_dividends_cached(self, cache_dir: Path) -> None:
        """Test that dividends are cached."""
        api_token = "test-token"
        route = respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/dividend"
        ).mock(return_value=Response(200, json=SAMPLE_DIVIDENDS_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            await client.stocks.get_dividends("FAKE1")
            await client.stocks.get_dividends("FAKE1")
            assert route.call_count == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_dividends_raw(self, cache_dir: Path) -> None:
        """Test fetching raw dividend data."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/dividend").mock(
            return_value=Response(200, json=SAMPLE_DIVIDENDS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            raw = await client.stocks.get_dividends_raw("FAKE1")
            # Real API returns array directly
            assert isinstance(raw, list)


class TestPriceHistoryEndpoint:
    """Tests for price history endpoint."""

    @pytest.fixture
    def cache_dir(self) -> Path:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_price_history(self, cache_dir: Path) -> None:
        """Test fetching price history returns typed model."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/price").mock(
            return_value=Response(200, json=SAMPLE_PRICE_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            prices = await client.stocks.get_price_history("FAKE1")

            assert isinstance(prices, PriceHistory)
            assert prices.symbol == "FAKE1"
            # Real API returns array of [date, price] tuples
            assert len(prices.prices) > 0

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_price_history_cached(self, cache_dir: Path) -> None:
        """Test that price history is cached."""
        api_token = "test-token"
        route = respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/price"
        ).mock(return_value=Response(200, json=SAMPLE_PRICE_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            await client.stocks.get_price_history("FAKE1")
            await client.stocks.get_price_history("FAKE1")
            assert route.call_count == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_price_history_raw(self, cache_dir: Path) -> None:
        """Test fetching raw price data."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/price").mock(
            return_value=Response(200, json=SAMPLE_PRICE_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            raw = await client.stocks.get_price_history_raw("FAKE1")
            # Real API returns array of [date, price] tuples
            assert isinstance(raw, list)

    @pytest.mark.asyncio
    @respx.mock
    async def test_price_point_data(self, cache_dir: Path) -> None:
        """Test that price points contain date and price."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/price").mock(
            return_value=Response(200, json=SAMPLE_PRICE_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            prices = await client.stocks.get_price_history("FAKE1")

            point = prices.prices[0]
            # Date should be converted to YYYY-MM-DD format
            assert point.date is not None
            assert point.price is not None


class TestInsiderTradesEndpoint:
    """Tests for insider trades endpoint."""

    @pytest.fixture
    def cache_dir(self) -> Path:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_insider_trades(self, cache_dir: Path) -> None:
        """Test fetching insider trades returns typed model."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/insider").mock(
            return_value=Response(200, json=SAMPLE_INSIDERS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            insiders = await client.stocks.get_insider_trades("FAKE1")

            assert isinstance(insiders, InsiderTrades)
            assert insiders.symbol == "FAKE1"
            # Real API returns {symbol: [trades]}
            assert len(insiders.trades) > 0

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_insider_trades_cached(self, cache_dir: Path) -> None:
        """Test that insider trades are cached."""
        api_token = "test-token"
        route = respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/insider"
        ).mock(return_value=Response(200, json=SAMPLE_INSIDERS_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            await client.stocks.get_insider_trades("FAKE1")
            await client.stocks.get_insider_trades("FAKE1")
            assert route.call_count == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_insider_trades_raw(self, cache_dir: Path) -> None:
        """Test fetching raw insider trades data."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/insider").mock(
            return_value=Response(200, json=SAMPLE_INSIDERS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            raw = await client.stocks.get_insider_trades_raw("FAKE1")
            assert isinstance(raw, dict)
            # Real API returns {symbol: [trades]}
            assert "FAKE1" in raw

    @pytest.mark.asyncio
    @respx.mock
    async def test_insider_trade_details(self, cache_dir: Path) -> None:
        """Test that individual trades contain expected details."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/insider").mock(
            return_value=Response(200, json=SAMPLE_INSIDERS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            insiders = await client.stocks.get_insider_trades("FAKE1")

            trade = insiders.trades[0]
            # Real API has: insider, position, date, type, trans_share, price
            assert trade.insider_name is not None
            assert trade.insider_title is not None
            assert trade.trade_date is not None


class TestModelsEdgeCases:
    """Tests for edge cases in model parsing."""

    def test_estimates_empty_response(self) -> None:
        """Test parsing empty estimates response."""
        estimates = AnalystEstimates.from_api_response({}, "TEST")
        assert estimates.symbol == "TEST"
        assert len(estimates.annual_estimates) == 0

    def test_dividends_empty_response(self) -> None:
        """Test parsing empty dividends response."""
        dividends = DividendHistory.from_api_response([], "TEST")
        assert dividends.symbol == "TEST"
        assert len(dividends.payments) == 0

    def test_price_history_empty_response(self) -> None:
        """Test parsing empty price history response."""
        prices = PriceHistory.from_api_response([], "TEST")
        assert prices.symbol == "TEST"
        assert len(prices.prices) == 0

    def test_insider_trades_empty_response(self) -> None:
        """Test parsing empty insider trades response."""
        insiders = InsiderTrades.from_api_response({}, "TEST")
        assert insiders.symbol == "TEST"
        assert len(insiders.trades) == 0
