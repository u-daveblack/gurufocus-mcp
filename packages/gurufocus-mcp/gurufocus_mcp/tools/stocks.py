"""Stock-related MCP tools.

Tools for fetching stock financial data from GuruFocus API.
"""

from typing import Annotated, Any, Literal, cast

from fastmcp import Context, FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

from gurufocus_api.logging import get_logger

from ..errors import raise_api_error, validate_symbol
from ..formatting import OutputFormat, format_output

logger = get_logger(__name__)


def register_stock_tools(mcp: FastMCP) -> None:
    """Register stock-related tools with the MCP server.

    Args:
        mcp: The FastMCP server instance to register tools with.
    """

    @mcp.tool
    async def get_stock_summary(
        symbol: Annotated[
            str,
            Field(description="Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"),
        ],
        format: Annotated[
            OutputFormat,
            Field(
                default="toon",
                description="Output format: 'toon' (default, token-efficient) or 'json' (standard)",
            ),
        ] = "toon",
        ctx: Context = None,  # type: ignore[assignment]
    ) -> str | dict[str, Any]:
        """Get comprehensive financial summary for a stock.

        Returns structured data including:
        - Company info: name, sector, industry, market cap, description
        - Current price and daily change percentage
        - Quality scores: GF Score, financial strength, profitability rank, growth rank
        - Valuation metrics: P/E, P/B, P/S ratios, GF Value, DCF estimates
        - Financial ratios with 5/10-year averages and industry medians
        - Institutional activity: guru and fund buying/selling percentages

        Use this tool when you need to analyze a stock's fundamentals,
        valuation, or financial health.

        The 'format' parameter controls output encoding:
        - 'toon': Token-efficient format (30-60% smaller), recommended for AI contexts
        - 'json': Standard JSON format for debugging or compatibility
        """
        normalized = validate_symbol(symbol)
        if not normalized:
            raise ToolError(
                f"Invalid symbol format: '{symbol}'. "
                "Please provide a valid stock ticker symbol (e.g., AAPL, MSFT)."
            )

        logger.debug("get_stock_summary_called", symbol=normalized, format=format)

        try:
            client = getattr(ctx.fastmcp, "state", {}).get("client")
            if client is None:
                raise ToolError(
                    "GuruFocus client not initialized. "
                    "Please ensure GURUFOCUS_API_TOKEN environment variable is set."
                )

            summary = await client.stocks.get_summary(normalized)
            data = cast(dict[str, Any], summary.model_dump(mode="json", exclude_none=True))
            logger.debug("get_stock_summary_success", symbol=normalized, format=format)
            return format_output(data, format)

        except ToolError:
            raise
        except Exception as e:
            logger.error("get_stock_summary_error", symbol=normalized, error=str(e))
            raise_api_error(e)

    @mcp.tool
    async def get_stock_financials(
        symbol: Annotated[
            str,
            Field(description="Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"),
        ],
        period_type: Annotated[
            Literal["annual", "quarterly"],
            Field(
                default="annual",
                description="Financial period type: 'annual' for yearly data or 'quarterly' for quarterly data",
            ),
        ] = "annual",
        format: Annotated[
            OutputFormat,
            Field(
                default="toon",
                description="Output format: 'toon' (default, token-efficient) or 'json' (standard)",
            ),
        ] = "toon",
        ctx: Context = None,  # type: ignore[assignment]
    ) -> str | dict[str, Any]:
        """Get financial statements for a stock.

        Returns historical financial data including:
        - Per-share metrics: revenue per share, EPS, book value per share, FCF per share
        - Income statement: revenue, gross profit, operating income, net income, EBITDA
        - Balance sheet: total assets, liabilities, equity, debt, cash
        - Cash flow: operating cash flow, capex, free cash flow, dividends paid
        - Margins: gross margin, operating margin, net margin

        Data is organized by fiscal period (most recent first) with both annual
        and quarterly options available.

        Use this tool when you need to analyze a company's financial performance
        over time, track revenue/earnings trends, or evaluate balance sheet health.

        The 'format' parameter controls output encoding:
        - 'toon': Token-efficient format (30-60% smaller), recommended for AI contexts
        - 'json': Standard JSON format for debugging or compatibility
        """
        normalized = validate_symbol(symbol)
        if not normalized:
            raise ToolError(
                f"Invalid symbol format: '{symbol}'. "
                "Please provide a valid stock ticker symbol (e.g., AAPL, MSFT)."
            )

        logger.debug(
            "get_stock_financials_called",
            symbol=normalized,
            period_type=period_type,
            format=format,
        )

        try:
            client = getattr(ctx.fastmcp, "state", {}).get("client")
            if client is None:
                raise ToolError(
                    "GuruFocus client not initialized. "
                    "Please ensure GURUFOCUS_API_TOKEN environment variable is set."
                )

            financials = await client.stocks.get_financials(normalized, period_type=period_type)
            data = cast(dict[str, Any], financials.model_dump(mode="json", exclude_none=True))
            logger.debug(
                "get_stock_financials_success",
                symbol=normalized,
                period_type=period_type,
                format=format,
            )
            return format_output(data, format)

        except ToolError:
            raise
        except Exception as e:
            logger.error("get_stock_financials_error", symbol=normalized, error=str(e))
            raise_api_error(e)

    @mcp.tool
    async def get_stock_keyratios(
        symbol: Annotated[
            str,
            Field(description="Stock ticker symbol (e.g., AAPL, MSFT, GOOGL)"),
        ],
        format: Annotated[
            OutputFormat,
            Field(
                default="toon",
                description="Output format: 'toon' (default, token-efficient) or 'json' (standard)",
            ),
        ] = "toon",
        ctx: Context = None,  # type: ignore[assignment]
    ) -> str | dict[str, Any]:
        """Get key financial ratios for a stock.

        Returns comprehensive financial ratios organized by category:
        - Quality scores: Piotroski F-Score, Altman Z-Score, GF Score, financial strength
        - Profitability: ROE, ROA, ROIC, gross/operating/net margins
        - Liquidity: current ratio, quick ratio, cash ratio
        - Solvency: debt-to-equity, debt-to-asset, interest coverage
        - Efficiency: asset turnover, inventory turnover, days sales outstanding
        - Growth: 1/3/5/10-year revenue, EPS, and FCF growth rates
        - Valuation: P/E, P/B, P/S, PEG, EV/EBITDA, GF Value
        - Price metrics: 52-week high/low, beta, volatility, returns
        - Dividends: yield, payout ratio, growth rates, years of consecutive growth

        Use this tool when you need to evaluate a company's financial health,
        compare it to peers, or assess investment quality across multiple dimensions.

        The 'format' parameter controls output encoding:
        - 'toon': Token-efficient format (30-60% smaller), recommended for AI contexts
        - 'json': Standard JSON format for debugging or compatibility
        """
        normalized = validate_symbol(symbol)
        if not normalized:
            raise ToolError(
                f"Invalid symbol format: '{symbol}'. "
                "Please provide a valid stock ticker symbol (e.g., AAPL, MSFT)."
            )

        logger.debug("get_stock_keyratios_called", symbol=normalized, format=format)

        try:
            client = getattr(ctx.fastmcp, "state", {}).get("client")
            if client is None:
                raise ToolError(
                    "GuruFocus client not initialized. "
                    "Please ensure GURUFOCUS_API_TOKEN environment variable is set."
                )

            keyratios = await client.stocks.get_keyratios(normalized)
            data = cast(dict[str, Any], keyratios.model_dump(mode="json", exclude_none=True))
            logger.debug("get_stock_keyratios_success", symbol=normalized, format=format)
            return format_output(data, format)

        except ToolError:
            raise
        except Exception as e:
            logger.error("get_stock_keyratios_error", symbol=normalized, error=str(e))
            raise_api_error(e)
