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
    ExecutiveList,
    GuruFocusClient,
    GuruTradesHistory,
    InsiderTrades,
    PriceHistory,
    StockGurusResponse,
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
SAMPLE_GURUS_RESPONSE = load_fixture("gurus")
SAMPLE_EXECUTIVES_RESPONSE = load_fixture("executives")
SAMPLE_TRADES_HISTORY_RESPONSE = load_fixture("trades_history")


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

    def test_gurus_empty_response(self) -> None:
        """Test parsing empty gurus response."""
        gurus = StockGurusResponse.from_api_response({}, "TEST")
        assert gurus.symbol == "TEST"
        assert len(gurus.picks) == 0
        assert len(gurus.holdings) == 0

    def test_executives_empty_response(self) -> None:
        """Test parsing empty executives response."""
        execs = ExecutiveList.from_api_response([], "TEST")
        assert execs.symbol == "TEST"
        assert len(execs.executives) == 0

    def test_trades_history_empty_response(self) -> None:
        """Test parsing empty trades history response."""
        trades = GuruTradesHistory.from_api_response([], "TEST")
        assert trades.symbol == "TEST"
        assert len(trades.periods) == 0


class TestGurusEndpoint:
    """Tests for gurus endpoint."""

    @pytest.fixture
    def cache_dir(self) -> Path:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_gurus(self, cache_dir: Path) -> None:
        """Test fetching gurus returns typed model."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/gurus").mock(
            return_value=Response(200, json=SAMPLE_GURUS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            gurus = await client.stocks.get_gurus("FAKE1")

            assert isinstance(gurus, StockGurusResponse)
            assert gurus.symbol == "FAKE1"
            # Response should have picks and holdings
            assert len(gurus.picks) > 0
            assert len(gurus.holdings) > 0

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_gurus_cached(self, cache_dir: Path) -> None:
        """Test that gurus are cached."""
        api_token = "test-token"
        route = respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/gurus"
        ).mock(return_value=Response(200, json=SAMPLE_GURUS_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            await client.stocks.get_gurus("FAKE1")
            await client.stocks.get_gurus("FAKE1")
            assert route.call_count == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_gurus_raw(self, cache_dir: Path) -> None:
        """Test fetching raw gurus data."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/gurus").mock(
            return_value=Response(200, json=SAMPLE_GURUS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            raw = await client.stocks.get_gurus_raw("FAKE1")
            assert isinstance(raw, dict)
            # API returns {symbol: {picks: [], holdings: []}}
            assert "FAKE1" in raw

    @pytest.mark.asyncio
    @respx.mock
    async def test_guru_pick_details(self, cache_dir: Path) -> None:
        """Test that individual picks contain expected details."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/gurus").mock(
            return_value=Response(200, json=SAMPLE_GURUS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            gurus = await client.stocks.get_gurus("FAKE1")

            pick = gurus.picks[0]
            assert pick.guru is not None
            assert pick.action is not None
            assert pick.date is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_guru_holding_details(self, cache_dir: Path) -> None:
        """Test that individual holdings contain expected details."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/gurus").mock(
            return_value=Response(200, json=SAMPLE_GURUS_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            gurus = await client.stocks.get_gurus("FAKE1")

            holding = gurus.holdings[0]
            assert holding.guru is not None
            assert holding.current_shares is not None
            assert holding.perc_assets is not None


class TestExecutivesEndpoint:
    """Tests for executives endpoint."""

    @pytest.fixture
    def cache_dir(self) -> Path:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_executives(self, cache_dir: Path) -> None:
        """Test fetching executives returns typed model."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/executives").mock(
            return_value=Response(200, json=SAMPLE_EXECUTIVES_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            execs = await client.stocks.get_executives("FAKE1")

            assert isinstance(execs, ExecutiveList)
            assert execs.symbol == "FAKE1"
            assert len(execs.executives) > 0

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_executives_cached(self, cache_dir: Path) -> None:
        """Test that executives are cached."""
        api_token = "test-token"
        route = respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/executives"
        ).mock(return_value=Response(200, json=SAMPLE_EXECUTIVES_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            await client.stocks.get_executives("FAKE1")
            await client.stocks.get_executives("FAKE1")
            assert route.call_count == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_executives_raw(self, cache_dir: Path) -> None:
        """Test fetching raw executives data."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/executives").mock(
            return_value=Response(200, json=SAMPLE_EXECUTIVES_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            raw = await client.stocks.get_executives_raw("FAKE1")
            # API returns array directly
            assert isinstance(raw, list)

    @pytest.mark.asyncio
    @respx.mock
    async def test_executive_details(self, cache_dir: Path) -> None:
        """Test that individual executives contain expected details."""
        api_token = "test-token"
        respx.get(f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/executives").mock(
            return_value=Response(200, json=SAMPLE_EXECUTIVES_RESPONSE)
        )

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            execs = await client.stocks.get_executives("FAKE1")

            exec = execs.executives[0]
            assert exec.name is not None
            assert exec.position is not None
            assert exec.transaction_date is not None


class TestTradesHistoryEndpoint:
    """Tests for trades history endpoint."""

    @pytest.fixture
    def cache_dir(self) -> Path:
        """Create a temporary cache directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_trades_history(self, cache_dir: Path) -> None:
        """Test fetching trades history returns typed model."""
        api_token = "test-token"
        respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/trades/history"
        ).mock(return_value=Response(200, json=SAMPLE_TRADES_HISTORY_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            trades = await client.stocks.get_trades_history("FAKE1")

            assert isinstance(trades, GuruTradesHistory)
            assert trades.symbol == "FAKE1"
            assert len(trades.periods) > 0

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_trades_history_cached(self, cache_dir: Path) -> None:
        """Test that trades history is cached."""
        api_token = "test-token"
        route = respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/trades/history"
        ).mock(return_value=Response(200, json=SAMPLE_TRADES_HISTORY_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            await client.stocks.get_trades_history("FAKE1")
            await client.stocks.get_trades_history("FAKE1")
            assert route.call_count == 1

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_trades_history_raw(self, cache_dir: Path) -> None:
        """Test fetching raw trades history data."""
        api_token = "test-token"
        respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/trades/history"
        ).mock(return_value=Response(200, json=SAMPLE_TRADES_HISTORY_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            raw = await client.stocks.get_trades_history_raw("FAKE1")
            # API returns array directly
            assert isinstance(raw, list)

    @pytest.mark.asyncio
    @respx.mock
    async def test_trades_history_period_details(self, cache_dir: Path) -> None:
        """Test that individual periods contain expected details."""
        api_token = "test-token"
        respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/trades/history"
        ).mock(return_value=Response(200, json=SAMPLE_TRADES_HISTORY_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            trades = await client.stocks.get_trades_history("FAKE1")

            period = trades.periods[0]
            assert period.symbol is not None
            assert period.portdate is not None
            assert period.buy_count >= 0
            assert period.sell_count >= 0

    @pytest.mark.asyncio
    @respx.mock
    async def test_trades_history_guru_actions(self, cache_dir: Path) -> None:
        """Test that guru buy/sell actions are parsed correctly."""
        api_token = "test-token"
        respx.get(
            f"https://api.gurufocus.com/public/user/{api_token}/stock/FAKE1/trades/history"
        ).mock(return_value=Response(200, json=SAMPLE_TRADES_HISTORY_RESPONSE))

        async with GuruFocusClient(
            api_token=api_token,
            cache_dir=str(cache_dir),
        ) as client:
            trades = await client.stocks.get_trades_history("FAKE1")

            # First period should have buy_gurus
            period = trades.periods[0]
            assert len(period.buy_gurus) > 0
            buyer = period.buy_gurus[0]
            assert buyer.guru_id > 0
            assert buyer.guru_name is not None
            assert buyer.share_change > 0  # Positive for buys
