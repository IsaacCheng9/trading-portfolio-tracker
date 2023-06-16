"""
Module containing functions relating to retrieving financial data from yahoo finance 
using yfinance and performing financial calculations 
"""

import requests
import yfinance as yf
import pandas as pd
from decimal import Decimal


def get_ticker(name: str) -> str:
    """
    Gets the ticker of a company given a name.
    Credit: https://gist.github.com/bruhbruhroblox/dd9d981c8c37983f61e423a45085e063

    Args:
      name: Name of the company/index.

    Returns:
      Ticker of the company.
    """
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    params = {"q": name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={"User-Agent": user_agent})
    data = res.json()

    company_code = data["quotes"][0]["symbol"]
    return company_code


def get_history(name: str, period: str = "1mo") -> pd.DataFrame:
    """
    Gets the stock history of a company or index given a name.

    Args:
      name: Name of the company/index.
      period: Duration in which you want to retrieve data.

    Returns:
      Historical data relating to the stock.
    """

    tick = yf.Ticker(get_ticker(name))
    return tick.history(period=period)


def get_info(name: str) -> dict[str, str]:
    """
    Returns information about a stock/company.
    Accounts for the difference in the yfinance library in returning
    information about different types of assets and assets which have a
    delay in reporting of price.

    Args:
      name: Name of the company/index/asset/...

    Returns:
      Dictionary containing information about the stock, future, or index.
    """
    # Creates a yfinance ticker object for a given asset
    try:
        ticker = yf.Ticker(get_ticker(name))
    except:
        return False

    # Creates a dictionary containing basic information about the asset
    return_dict = {
        "name": ticker.info["shortName"],
        "ticker": ticker.info["symbol"],
        "type": ticker.info["quoteType"],
    }

    if return_dict["type"] in ["INDEX", "FUTURE", "CRYPTOCURRENCY"]:
        # Downloads the most recent data about the price of the asset
        data = yf.download(return_dict["ticker"], period="1d", interval="1m", progress=False)
        last_row_index = len(data) - 1
        # Gets the last reported close price of the asset
        last_row_open_value = data.iloc[last_row_index]["Close"]
        return_dict["current_value"] = last_row_open_value
        return_dict["currency"] = ticker.info["currency"]
    else:  # If the asset is a stock
        return_dict["current_value"] = ticker.info["currentPrice"]
        return_dict["sector"] = ticker.info["sector"]
        return_dict["currency"] = ticker.info["financialCurrency"]
    return return_dict


def get_absolute_rate_of_return(current: Decimal, purchase: Decimal) -> Decimal:
    """
    Calculates the absolute rate of return given the current and purchase price of an
    asset.

    Args:
      current: Current price of asset.
      purchase: Purchase price of asset.

    Returns:
      absolute rate of return.
    """
    return ((current - purchase) / purchase) * 100


if __name__ == "__main__":
    print(get_info("FTSE 250"))
    print(get_info("Apple"))
    print(get_info("Ethereum"))
