"""Pydantic models for dividend data."""

from contextlib import suppress
from typing import Any

from pydantic import BaseModel, Field


class DividendPayment(BaseModel):
    """A single dividend payment."""

    ex_date: str | None = Field(default=None, description="Ex-dividend date (YYYY-MM-DD)")
    record_date: str | None = Field(default=None, description="Record date (YYYY-MM-DD)")
    pay_date: str | None = Field(default=None, description="Payment date (YYYY-MM-DD)")
    amount: float | None = Field(default=None, description="Dividend amount per share")
    currency: str | None = Field(default=None, description="Currency of payment")
    dividend_type: str | None = Field(default=None, description="Type (e.g., 'Cash Div.')")


class DividendHistory(BaseModel):
    """Dividend history for a stock.

    Contains historical payment records (most recent first).
    """

    symbol: str = Field(description="Stock ticker symbol")

    # Historical payments
    payments: list[DividendPayment] = Field(
        default_factory=list, description="Historical dividend payments (most recent first)"
    )

    @classmethod
    def from_api_response(cls, data: dict[str, Any], symbol: str) -> "DividendHistory":
        """Create DividendHistory from raw API response.

        Args:
            data: Raw JSON response from the API - may contain dividend data nested
            symbol: Stock ticker symbol

        Returns:
            Populated DividendHistory instance
        """
        payments: list[DividendPayment] = []

        # Handle different API response structures
        dividend_data: list[dict[str, Any]] = []
        if isinstance(data, list):
            dividend_data = data
        elif isinstance(data, dict):
            # Try common keys where dividend data might be nested
            dividend_data = (
                data.get("dividends", [])
                or data.get("data", [])
                or (next(iter(data.values())) if data else [])
            )
            if not isinstance(dividend_data, list):
                dividend_data = []

        for item in dividend_data:
            if isinstance(item, dict):
                payments.append(_parse_dividend_payment(item))

        return cls(
            symbol=symbol,
            payments=payments,
        )


def _parse_dividend_payment(data: dict[str, Any]) -> DividendPayment:
    """Parse a single dividend payment from API data."""
    amount_str = data.get("amount")
    amount = None
    if amount_str is not None:
        with suppress(TypeError, ValueError):
            amount = float(amount_str)

    return DividendPayment(
        ex_date=data.get("ex_date"),
        record_date=data.get("record_date"),
        pay_date=data.get("pay_date"),
        amount=amount,
        currency=data.get("currency"),
        dividend_type=data.get("type"),
    )
