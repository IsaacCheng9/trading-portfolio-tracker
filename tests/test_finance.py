import pytest
import pandas as pd

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
    """ """
    symbol = finance.get_symbol(name)
    assert type(symbol) is str
    assert symbol == expected_result


def test_get_symbol_invalid() -> None:
    """ """
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
    """ """
    name = finance.get_name_from_symbol(symbol)
    assert type(name) is str
    assert name == expected_result


def test_get_name_from_symbol_invalid() -> None:
    """ """
    name = finance.get_name_from_symbol("INVALID")
    assert type(name) == str
    assert name == ""


@pytest.mark.parametrize(
    "name", [("Tesla"), ("FTSE 100"), ("T. Rowe Price Funds OEIC Asian ")]
)
def test_get_history_valid(name: str) -> None:
    """ """
    history = finance.get_history(name)
    assert history is not None
    assert type(history) is pd.DataFrame


def test_get_history_invalid() -> None:
    pass
