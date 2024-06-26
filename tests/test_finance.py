import os
from decimal import Decimal

import duckdb
import pandas as pd
import pytest
import yfinance as yf

from src.trading_portfolio_tracker import app, finance

DB_PATH = "resources/test.db"


@pytest.fixture
def setup_and_teardown_database():
    """ """
    app.create_database_tables(DB_PATH)
    yield
    os.remove(DB_PATH)


@pytest.mark.parametrize(
    "name, expected_result",
    [
        ("Apple", "AAPL"),
        ("FTSE 100", "^FTSE"),
    ],
)
def test_get_symbol_valid(name: str, expected_result: str) -> None:
    """
    Tests the get_symbol method with valid company/index/fund names to assert
    the correct symbol is returned.

    Args:
        name: Name of the company/index/fund.
        expected_result: Expected symbol to be returned (AAPL...).
    """
    symbol = finance.get_symbol(name)
    assert isinstance(symbol, str)
    assert symbol == expected_result


def test_get_symbol_invalid() -> None:
    """
    Tests the get_symbol method with an invalid name to assert an appropriate
    error is thrown.
    """
    try:
        finance.get_symbol("Invalid")
        assert False
    except IndexError:
        assert True


@pytest.mark.parametrize(
    "symbol, expected_result",
    [
        ("TSLA", "Tesla, Inc."),
        ("^FTSE", "FTSE 100"),
    ],
)
def test_get_name_from_symbol_valid(symbol: str, expected_result: str) -> None:
    """
    Tests the get_name_from_symbol method with valid company/index/fund symbols
    to ensure the correct associated name is returned.

    Args:
        symbol: Company/index/fund symbol.
        expected_result: Expected name to be returned.
    """
    name = finance.get_name_from_symbol(symbol)
    assert isinstance(name, str)
    assert name == expected_result


def test_get_name_from_symbol_invalid() -> None:
    """
    Tests get_name_from_symbol using an invalid symbol to ensure a
    blank name is returned.
    """
    name = finance.get_name_from_symbol("INVALID")
    assert isinstance(name, str)
    assert name == ""


@pytest.mark.parametrize(
    "name",
    [
        "Tesla",
        "FTSE 100",
    ],
)
def test_get_history_valid(name: str) -> None:
    """
    Tests the get_history method with valid names to ensure
    the recent pricing history of each is returned.

    Args:
        name: Name of the company/index/OEIC.
    """
    history = finance.get_history(name)
    assert history is not None
    assert type(history) is pd.DataFrame


def test_get_history_invalid() -> None:
    """
    Tests the get_history method with an invalid company name to ensure
    an error is thrown and no data is returned.
    """
    try:
        finance.get_history("INVALID")
        assert False
    except IndexError:
        assert True


@pytest.mark.parametrize(
    "symbol, expected_type, expected_currency",
    [
        ("AAPL", "EQUITY", "USD"),
        ("0P0001BVXP.L", "MUTUALFUND", "GBP"),
        ("^FTSE", "INDEX", "GBP"),
    ],
)
def test_get_info_valid(
    symbol: str, expected_type: str, expected_currency: str
) -> None:
    """
    Tests the get_info method using valid symbols to ensure pricing data
    and information about the index/company/OEIC is retrieved.

    Args:
        symbol: Listed symbol.
        expected_type: Expected type of the asset (Equity, Index, Mutual Fund).
        expected_currency: Expected currency the asset is traded in.
    """
    info = finance.get_info(symbol)
    assert info["currency"] == expected_currency
    assert info["type"] == expected_type
    assert float(info["current_value"]) >= 0.0


def test_get_info_lse() -> None:
    """
    Tests the get_info method using a stock listed on the London Stock Exchange
    to ensure that GBX is converted to GBP.
    """
    symbol = "LSEG.L"
    ticker = yf.Ticker(symbol)
    info = finance.get_info(symbol)
    assert info["current_value"] == (ticker.info["currentPrice"] / 100)
    assert info["currency"] == "GBP"


def test_get_info_invalid() -> None:
    """
    Tests the get_info method using an invalid symbol to ensure an error is
    thrown.
    """
    with pytest.raises(KeyError):
        finance.get_info("INVALID")


@pytest.mark.parametrize(
    "current, purchase, expected_result",
    [
        (10, 5, 100),
        (5, 10, -50),
        (0, 0, 0),
    ],
)
def test_get_rate_of_return_valid(
    current: float, purchase: float, expected_result: float
) -> None:
    """
    Tests the get_rate_of_return method using valid current and
    purchase prices of an asset.

    Args:
        current: Current price of the asset.
        purchase: Purchase price of the asset.
        expected_result: Expected absolute rate of return
    """
    calculated_ror = finance.get_rate_of_return(Decimal(current), Decimal(purchase))
    assert calculated_ror == expected_result


def test_get_rate_of_return_no_purchase_price() -> None:
    """
    Tests the get_rate_of_return method whilst passing no purchase
    price into the method.
    """
    calculated_ror = finance.get_rate_of_return(Decimal(100), Decimal(0))
    assert calculated_ror == 0


def test_get_rate_of_return_invalid() -> None:
    """
    Tests the get_rate_of_return method whilst passing no purchase
    and current price into the method
    """
    calculated_ror = finance.get_rate_of_return(Decimal(0), Decimal(0))
    assert calculated_ror == 0


def test_upsert_transaction_into_portfolio_valid_buy(
    setup_and_teardown_database,
) -> None:
    """ """
    finance.upsert_transaction_into_portfolio(
        "buy", "BTC-USD", "USD", Decimal(1000), Decimal(100), Decimal(100), DB_PATH
    )

    with duckdb.connect(DB_PATH) as conn:
        result = conn.execute(
            "SELECT symbol, name, units, currency, paid, paid_gbp FROM portfolio "
            "WHERE symbol = ?",
            ("BTC-USD",),
        ).fetchone()

    if result:
        symbol, _, units, currency, paid, _ = result
        assert symbol == "BTC-USD"
        assert float(units) == 10
        assert currency == "USD"
        assert float(paid) == 1000
    else:
        assert False


def test_upsert_transaction_into_portfolio_valid_sell(
    setup_and_teardown_database,
) -> None:
    pass


def test_upsert_transaction_into_portfolio_invalid_sell(
    setup_and_teardown_database,
) -> None:
    """ """
    pass


def test_remove_security_from_portfolio_valid(setup_and_teardown_database) -> None:
    """ """
    pass


def test_remove_security_from_portfolio_invalid(setup_and_teardown_database) -> None:
    """ """
    pass


def test_get_total_paid_into_portfolio_valid(setup_and_teardown_database) -> None:
    """ """
    pass


def test_get_total_paid_into_portfolio_empty(setup_and_teardown_database) -> None:
    """ """
    pass


@pytest.mark.parametrize(
    "original_currency, currency_to", [("GBP", "USD"), ("USD", "JPY"), ("JPY", "GBP")]
)
def test_get_exchange_rate_valid(original_currency: str, currency_to: str) -> None:
    """
    Tests the get_exchange_rate method providing valid currencies to ensure
    the most recent exchange rate is retrieved.

    Args:
        original_currency: Currency to convert from.
        currency_to: Currency to convert to.
    """
    exch_rate = finance.get_exchange_rate(original_currency, currency_to)
    assert exch_rate
    assert exch_rate > 0


@pytest.mark.parametrize(
    "currency",
    [
        "GBP",
        "EUR",
        "USD",
    ],
)
def test_get_exchange_rate_same_currency(currency: str) -> None:
    """
    Tests the get_exchange_rate method providing the same currency to convert
    to. The exchange rate between the same currency should be 1.

    Args:
        currency: Currency to convert from and to.
    """
    assert finance.get_exchange_rate(currency, currency) == 1


@pytest.mark.parametrize(
    "provided_date",
    [
        "1999-01-04",
        "2023-07-01",
        "2002-08-03",
    ],
)
def test_get_exchange_rate_valid_date(provided_date: str) -> None:
    """
    Tests the get_exchange_rate method providing a valid date.

    Args:
        provided_date: Date to retrieve the exchange rate from.
    """
    exch_rate = finance.get_exchange_rate("GBP", "USD", provided_date)
    assert exch_rate
    assert exch_rate > 0


def test_get_exchange_rate_too_old_date() -> None:
    """
    Tests the get_exchange_rate method providing a date that is too old for
    the Frankfurter API to ensure the oldest possible exchange rate is
    retrieved.
    """
    exch_rate = finance.get_exchange_rate("GBP", "USD", "1900-01-01")
    exch_rate_oldest = finance.get_exchange_rate("GBP", "USD", "1999-01-04")

    assert exch_rate == exch_rate_oldest


def test_get_exchange_rate_invalid_date() -> None:
    """
    Tests the get_exchange_rate method providing an invalid date.
    """
    try:
        finance.get_exchange_rate("GBP", "USD", "INVALID")
        assert False
    except ValueError:
        assert True
