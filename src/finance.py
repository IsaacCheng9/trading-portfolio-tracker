"""
Module containing functions relating to 
https://pypi.org/project/yfinance/
"""

import requests
import yfinance as yf
import pandas as pd


def get_ticker(name: str) -> str:
    """
    Gets the ticker of a company given a name.
    Credit: https://gist.github.com/bruhbruhroblox/dd9d981c8c37983f61e423a45085e063

    Args:
      name: Name of the company/Index.

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


def get_history(
    name: str,
    period: str = "1mo",
) -> pd.DataFrame:
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

    Args:
      name: Name of the company/index/...

    Returns:
      dictionary containing information about the stock, future, or index
    """
    ticker = yf.Ticker(get_ticker(name))
    if ticker:
        print(ticker.info)
        return_dict = {
            "name": ticker.info["shortName"],
            "type": ticker.info["quoteType"],
            "previous_close": ticker.info["previousClose"],
        }

        if return_dict["type"] in ["INDEX", "FUTURE"]:
            return_dict["open"] = ticker.info["open"]
            return_dict["currency"] = ticker.info["currency"]

        else:
            return_dict["current_value"] = ticker.info["currentPrice"]
            return_dict["sector"] = ticker.info["sector"]
            return_dict["currency"] = (ticker.info["financialCurrency"],)
        return return_dict
    else:
        return False


def absolute_rate_of_return(current: float, purchase: float) -> float:
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
