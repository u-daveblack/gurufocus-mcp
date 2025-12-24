"""Stock-related API endpoints."""

from typing import TYPE_CHECKING, Any, Literal, cast

from ..cache.config import CacheCategory
from ..models.dividends import DividendHistory
from ..models.estimates import AnalystEstimates
from ..models.financials import FinancialStatements
from ..models.insiders import InsiderTrades
from ..models.keyratios import KeyRatios
from ..models.price import PriceHistory
from ..models.summary import StockSummary

if TYPE_CHECKING:
    from ..client import GuruFocusClient


class StocksEndpoint:
    """Endpoints for stock data retrieval.

    This class provides methods for fetching stock information
    from the GuruFocus API with automatic caching support.

    Example:
        async with GuruFocusClient() as client:
            summary = await client.stocks.get_summary("AAPL")
            print(f"{summary.company_name}: {summary.gf_score.gf_score}")

            # Force fresh data (bypass cache)
            fresh = await client.stocks.get_summary("AAPL", bypass_cache=True)
    """

    def __init__(self, client: "GuruFocusClient") -> None:
        """Initialize the stocks endpoint.

        Args:
            client: The parent GuruFocusClient instance
        """
        self._client = client

    async def get_summary(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> StockSummary:
        """Get comprehensive summary for a stock.

        Retrieves general information, current price, valuation metrics,
        and quality scores for the specified stock.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            StockSummary with company info, price, valuation, and GF scores

        Raises:
            InvalidSymbolError: If the symbol is not found
            AuthenticationError: If the API token is invalid
            APIError: For other API errors

        Example:
            summary = await client.stocks.get_summary("AAPL")
            print(f"Company: {summary.company_name}")
            print(f"Price: ${summary.price.current}")
            print(f"GF Score: {summary.gf_score.gf_score}/100")
        """
        data = await self.get_summary_raw(symbol, bypass_cache=bypass_cache)
        return StockSummary.from_api_response(data, symbol.upper().strip())

    async def get_summary_raw(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> dict[str, Any]:
        """Get raw summary data for a stock.

        Same as get_summary() but returns the raw API response
        without parsing into a Pydantic model.

        Args:
            symbol: Stock ticker symbol
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            Raw JSON response as a dictionary
        """
        symbol = symbol.upper().strip()
        cache = self._client.cache

        # Try to get from cache first
        if not bypass_cache:
            cached_data = await cache.get(CacheCategory.SUMMARY, symbol)
            if cached_data is not None:
                return cast(dict[str, Any], cached_data)

        # Fetch from API
        data = await self._client.get(f"stock/{symbol}/summary")

        # Cache the response
        await cache.set(CacheCategory.SUMMARY, symbol, value=data)

        return cast(dict[str, Any], data)

    async def get_keyratios(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> KeyRatios:
        """Get key financial ratios for a stock.

        Retrieves comprehensive financial ratios including profitability,
        liquidity, solvency, efficiency, and growth metrics.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            KeyRatios with categorized financial ratios

        Raises:
            InvalidSymbolError: If the symbol is not found
            AuthenticationError: If the API token is invalid
            APIError: For other API errors

        Example:
            ratios = await client.stocks.get_keyratios("AAPL")
            print(f"ROE: {ratios.profitability.roe}%")
            print(f"Current Ratio: {ratios.liquidity.current_ratio}")
            print(f"Debt/Equity: {ratios.solvency.debt_to_equity}")
        """
        data = await self.get_keyratios_raw(symbol, bypass_cache=bypass_cache)
        return KeyRatios.from_api_response(data, symbol.upper().strip())

    async def get_keyratios_raw(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> dict[str, Any]:
        """Get raw key ratios data for a stock.

        Same as get_keyratios() but returns the raw API response
        without parsing into a Pydantic model.

        Args:
            symbol: Stock ticker symbol
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            Raw JSON response as a dictionary
        """
        symbol = symbol.upper().strip()
        cache = self._client.cache

        # Try to get from cache first
        if not bypass_cache:
            cached_data = await cache.get(CacheCategory.KEY_RATIOS, symbol)
            if cached_data is not None:
                return cast(dict[str, Any], cached_data)

        # Fetch from API
        data = await self._client.get(f"stock/{symbol}/keyratios")

        # Cache the response
        await cache.set(CacheCategory.KEY_RATIOS, symbol, value=data)

        return cast(dict[str, Any], data)

    async def get_financials(
        self,
        symbol: str,
        period_type: Literal["annual", "quarterly"] = "annual",
        bypass_cache: bool = False,
    ) -> FinancialStatements:
        """Get financial statements for a stock.

        Retrieves income statement, balance sheet, and cash flow statement
        data for multiple historical periods.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
            period_type: 'annual' for yearly data, 'quarterly' for quarterly
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            FinancialStatements with income, balance, and cash flow data

        Raises:
            InvalidSymbolError: If the symbol is not found
            AuthenticationError: If the API token is invalid
            APIError: For other API errors

        Example:
            financials = await client.stocks.get_financials("AAPL")
            latest_income = financials.income_statements[0]
            print(f"Revenue: ${latest_income.revenue:,.0f}")
            print(f"Net Income: ${latest_income.net_income:,.0f}")

            # Get quarterly data
            quarterly = await client.stocks.get_financials("AAPL", period_type="quarterly")
        """
        data = await self.get_financials_raw(
            symbol, period_type=period_type, bypass_cache=bypass_cache
        )
        return FinancialStatements.from_api_response(data, symbol.upper().strip(), period_type)

    async def get_financials_raw(
        self,
        symbol: str,
        period_type: Literal["annual", "quarterly"] = "annual",
        bypass_cache: bool = False,
    ) -> dict[str, Any]:
        """Get raw financial statements data for a stock.

        Same as get_financials() but returns the raw API response
        without parsing into a Pydantic model.

        Args:
            symbol: Stock ticker symbol
            period_type: 'annual' for yearly data, 'quarterly' for quarterly
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            Raw JSON response as a dictionary
        """
        symbol = symbol.upper().strip()
        cache = self._client.cache
        cache_key_suffix = f"{symbol}:{period_type}"

        # Try to get from cache first
        if not bypass_cache:
            cached_data = await cache.get(CacheCategory.FINANCIALS, cache_key_suffix)
            if cached_data is not None:
                return cast(dict[str, Any], cached_data)

        # Build API endpoint
        endpoint = f"stock/{symbol}/financials"
        params = {"type": period_type} if period_type == "quarterly" else None

        # Fetch from API
        data = await self._client.get(endpoint, params=params)

        # Cache the response
        await cache.set(CacheCategory.FINANCIALS, cache_key_suffix, value=data)

        return cast(dict[str, Any], data)

    async def get_analyst_estimates(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> AnalystEstimates:
        """Get analyst estimates and ratings for a stock.

        Retrieves analyst EPS/revenue estimates for upcoming periods
        and recommendation ratings.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            AnalystEstimates with ratings and forward estimates

        Raises:
            InvalidSymbolError: If the symbol is not found
            AuthenticationError: If the API token is invalid
            APIError: For other API errors

        Example:
            estimates = await client.stocks.get_analyst_estimates("AAPL")
            print(f"Rating: {estimates.ratings.rating}")
            print(f"Target Price: ${estimates.ratings.target_price}")
            for est in estimates.annual_estimates:
                print(f"{est.period}: EPS ${est.eps_estimate}")
        """
        data = await self.get_analyst_estimates_raw(symbol, bypass_cache=bypass_cache)
        return AnalystEstimates.from_api_response(data, symbol.upper().strip())

    async def get_analyst_estimates_raw(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> dict[str, Any]:
        """Get raw analyst estimates data for a stock.

        Same as get_analyst_estimates() but returns the raw API response
        without parsing into a Pydantic model.

        Args:
            symbol: Stock ticker symbol
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            Raw JSON response as a dictionary
        """
        symbol = symbol.upper().strip()
        cache = self._client.cache

        # Try to get from cache first
        if not bypass_cache:
            cached_data = await cache.get(CacheCategory.ESTIMATES, symbol)
            if cached_data is not None:
                return cast(dict[str, Any], cached_data)

        # Fetch from API
        data = await self._client.get(f"stock/{symbol}/analyst_estimate")

        # Cache the response
        await cache.set(CacheCategory.ESTIMATES, symbol, value=data)

        return cast(dict[str, Any], data)

    async def get_dividends(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> DividendHistory:
        """Get dividend history for a stock.

        Retrieves dividend payment history and summary metrics
        including yield, growth rates, and payout ratio.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            DividendHistory with summary metrics and payment history

        Raises:
            InvalidSymbolError: If the symbol is not found
            AuthenticationError: If the API token is invalid
            APIError: For other API errors

        Example:
            dividends = await client.stocks.get_dividends("AAPL")
            print(f"Yield: {dividends.summary.dividend_yield}%")
            print(f"Years of Growth: {dividends.summary.years_of_growth}")
            for payment in dividends.payments[:5]:
                print(f"{payment.ex_date}: ${payment.amount}")
        """
        data = await self.get_dividends_raw(symbol, bypass_cache=bypass_cache)
        return DividendHistory.from_api_response(data, symbol.upper().strip())

    async def get_dividends_raw(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> dict[str, Any]:
        """Get raw dividend data for a stock.

        Same as get_dividends() but returns the raw API response
        without parsing into a Pydantic model.

        Args:
            symbol: Stock ticker symbol
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            Raw JSON response as a dictionary
        """
        symbol = symbol.upper().strip()
        cache = self._client.cache

        # Try to get from cache first
        if not bypass_cache:
            cached_data = await cache.get(CacheCategory.DIVIDENDS, symbol)
            if cached_data is not None:
                return cast(dict[str, Any], cached_data)

        # Fetch from API
        data = await self._client.get(f"stock/{symbol}/dividend")

        # Cache the response
        await cache.set(CacheCategory.DIVIDENDS, symbol, value=data)

        return cast(dict[str, Any], data)

    async def get_price_history(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> PriceHistory:
        """Get historical price data for a stock.

        Retrieves daily OHLCV price data and summary statistics
        including returns over various periods.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            PriceHistory with statistics and daily price bars

        Raises:
            InvalidSymbolError: If the symbol is not found
            AuthenticationError: If the API token is invalid
            APIError: For other API errors

        Example:
            prices = await client.stocks.get_price_history("AAPL")
            print(f"Current: ${prices.statistics.current_price}")
            print(f"52-Week High: ${prices.statistics.high_52week}")
            print(f"YTD Return: {prices.statistics.change_ytd}%")
            for bar in prices.prices[:5]:
                print(f"{bar.date}: ${bar.close}")
        """
        data = await self.get_price_history_raw(symbol, bypass_cache=bypass_cache)
        return PriceHistory.from_api_response(data, symbol.upper().strip())

    async def get_price_history_raw(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> dict[str, Any]:
        """Get raw price history data for a stock.

        Same as get_price_history() but returns the raw API response
        without parsing into a Pydantic model.

        Args:
            symbol: Stock ticker symbol
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            Raw JSON response as a dictionary
        """
        symbol = symbol.upper().strip()
        cache = self._client.cache

        # Try to get from cache first
        if not bypass_cache:
            cached_data = await cache.get(CacheCategory.PRICE_HISTORY, symbol)
            if cached_data is not None:
                return cast(dict[str, Any], cached_data)

        # Fetch from API
        data = await self._client.get(f"stock/{symbol}/price")

        # Cache the response
        await cache.set(CacheCategory.PRICE_HISTORY, symbol, value=data)

        return cast(dict[str, Any], data)

    async def get_insider_trades(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> InsiderTrades:
        """Get insider trading activity for a stock.

        Retrieves recent insider transactions including buys, sells,
        and option exercises by company insiders.

        Args:
            symbol: Stock ticker symbol (e.g., "AAPL", "MSFT")
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            InsiderTrades with summary metrics and transaction history

        Raises:
            InvalidSymbolError: If the symbol is not found
            AuthenticationError: If the API token is invalid
            APIError: For other API errors

        Example:
            insiders = await client.stocks.get_insider_trades("AAPL")
            print(f"Net Shares (3M): {insiders.summary.net_shares_3m}")
            for trade in insiders.trades[:5]:
                print(f"{trade.trade_date}: {trade.insider_name} "
                      f"{trade.transaction_type} {trade.shares} shares")
        """
        data = await self.get_insider_trades_raw(symbol, bypass_cache=bypass_cache)
        return InsiderTrades.from_api_response(data, symbol.upper().strip())

    async def get_insider_trades_raw(
        self,
        symbol: str,
        bypass_cache: bool = False,
    ) -> dict[str, Any]:
        """Get raw insider trades data for a stock.

        Same as get_insider_trades() but returns the raw API response
        without parsing into a Pydantic model.

        Args:
            symbol: Stock ticker symbol
            bypass_cache: If True, skip cache and fetch fresh data

        Returns:
            Raw JSON response as a dictionary
        """
        symbol = symbol.upper().strip()
        cache = self._client.cache

        # Try to get from cache first
        if not bypass_cache:
            cached_data = await cache.get(CacheCategory.INSIDERS, symbol)
            if cached_data is not None:
                return cast(dict[str, Any], cached_data)

        # Fetch from API
        data = await self._client.get(f"stock/{symbol}/insider")

        # Cache the response
        await cache.set(CacheCategory.INSIDERS, symbol, value=data)

        return cast(dict[str, Any], data)
