import pytest
import pandas as pd
import yfinance as yf

from requests import exceptions
from src import finance


@pytest.mark.parametrize(
    "name, expected_result",
    [
        ("Apple", "AAPL"),
        ("FTSE 100", "^FTSE"),
        (
            "T. Rowe Price Funds OEIC Asian Opportunities Equity Fund Class C GBP",
            "0P0001BVXP.L",
        ),
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
    assert type(symbol) is str
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
        (
            "0P0001BVXP.L",
            "T. Rowe Price Funds OEIC Asian Opportunities Equity Fund Class C GBP",
        ),
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
    assert type(name) is str
    assert name == expected_result


def test_get_name_from_symbol_invalid() -> None:
    """
    Tests get_name_from_symbol using an invalid symbol to ensure a
    blank name is returned.
    """
    name = finance.get_name_from_symbol("INVALID")
    assert type(name) == str
    assert name == ""


@pytest.mark.parametrize(
    "name",
    [
        ("Tesla"),
        ("FTSE 100"),
        ("T. Rowe Price Funds OEIC Asian Opportunities Equity Fund Class C GBP"),
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
    assert info["current_value"] >= 0


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
    try:
        finance.get_info("INVALID")
        assert False
    except exceptions.HTTPError:
        assert True


@pytest.mark.parametrize(
    "current, purchase, expected_result",
    [
        (10, 5, 100),
        (5, 10, -50),
        (0, 0, 0),
    ],
)
def test_get_absolute_rate_of_return_valid(
    current: float, purchase: float, expected_result: float
) -> None:
    """
    Tests the get_absolute_rate_of_return method using valid current and
    purchase prices of an asset.

    Args:
        current: Current price of the asset.
        purchase: Purchase price of the asset.
        expected_result: Expected absolute rate of return
    """
    calculated_ror = finance.get_absolute_rate_of_return(current, purchase)
    assert calculated_ror == expected_result


def test_get_absolute_rate_of_return_no_purchase_price() -> None:
    """
    Tests the get_absolute_rate_of_return method whilst passing no purchase
    price into the method.
    """
    calculated_ror = finance.get_absolute_rate_of_return(100, None)
    assert calculated_ror == 0
