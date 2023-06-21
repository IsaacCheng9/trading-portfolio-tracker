"""
Module containing functions relating to retrieving financial data from yahoo finance 
using yfinance and performing financial calculations 
"""

import duckdb
import requests
import yfinance as yf
import pandas as pd
from decimal import Decimal
from requests import exceptions
from datetime import datetime, date

DB_PATH = "resources/portfolio.db"


def get_symbol(name: str) -> str:
    """
    Gets the symbol of a company given a name.
    Credit: https://gist.github.com/bruhbruhroblox/dd9d981c8c37983f61e423a45085e063

    Args:
        name: Name of the company/index.

    Returns:
        Symbol of the company.
    """
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    params = {"q": name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={"User-Agent": user_agent})
    data = res.json()

    company_code = data["quotes"][0]["symbol"]
    return company_code


def get_name_from_symbol(symbol: str) -> str:
    """
    Gets the name of the security given a symbol.

    Args:
        symbol: Symbol of the security.

    Returns:
        Name of the security.
    """
    tick = yf.Ticker(symbol)
    try:
        name = tick.info["shortName"]
        return name
    except (exceptions.HTTPError, KeyError):
        return ""


def get_history(name: str, period: str = "1mo") -> pd.DataFrame:
    """
    Gets the stock history of a company or index given a name.

    Args:
        name: Name of the company/index.
        period: Duration in which you want to retrieve data.

    Returns:
        Historical data relating to the stock.
    """

    tick = yf.Ticker(get_symbol(name))
    return tick.history(period=period)


def get_info(symbol: str) -> dict[str, str]:
    """
    Returns information about a stock/company.
    Accounts for the difference in the yfinance library in returning
    information about different types of assets and assets which have a
    delay in reporting of price.

    Args:
        symbol: Symbol of the company/index/asset/...

    Returns:
        Dictionary containing information about the stock, future, or index.
    """
    # Creates a yfinance ticker object for a given asset.
    try:
        ticker = yf.Ticker(symbol)
    except:
        return False

    # Creates a dictionary containing basic information about the asset.
    return_dict = {
        "name": ticker.info["shortName"],
        "ticker": ticker.info["symbol"],
        "type": ticker.info["quoteType"],
    }

    # Gets information about a given index, security, or stock.
    try:
        return_dict["current_value"] = ticker.info["currentPrice"]
        return_dict["currency"] = ticker.info["financialCurrency"]
        return_dict["sector"] = ticker.info["sector"]
    except:
        data = yf.download(return_dict["ticker"], period="1d", progress=False)
        last_row_index = len(data) - 1
        # Gets the last reported close price of the asset
        last_row_open_value = data.iloc[last_row_index]["Close"]
        return_dict["current_value"] = last_row_open_value
        return_dict["currency"] = ticker.info["currency"]

    # Checks if the stock is traded on the LSE, if so GBP is converted to GBX.
    if ticker.info["symbol"][-2:] == ".L":
        return_dict["current_value"] = ticker.info["currentPrice"] / 100
        return_dict["currency"] = "GBP"

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


def upsert_transaction_into_portfolio(
    type: str,
    symbol: str,
    currency: str,
    amount: Decimal,
    unit_price: Decimal,
) -> None:
    """
    Update/insert the portfolio based on a new transaction.

    Args:
        type: The type of transaction (Buy/Sell).
        symbol: The symbol of the security.
        currency: The currency of the security.
        amount: The amount of the transaction.
        unit_price: The unit price of the security.
        paid_standard_currency: The amount of the transaction after conversion to a currency.
    """
    # Search for the security in the portfolio.
    with duckdb.connect(database=DB_PATH) as conn:
        # Retrieve the security from the portfolio table based on the symbol
        result = conn.execute(
            "SELECT symbol, name, units, currency, paid FROM portfolio "
            "WHERE symbol = ?",
            (symbol,),
        ).fetchone()

    # Create a new HeldSecurity object for the transaction and save it if it
    # wasn't previously held.
    if not result:
        if type == "Sell":
            raise Exception("Cannot sell a security that is not held.")

        name = get_name_from_symbol(symbol)
        units = Decimal(amount / unit_price)
        with duckdb.connect(database=DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO portfolio VALUES (?, ?, ?, ?, ?)",
                (
                    symbol,
                    name,
                    str(units),
                    currency,
                    str(amount),
                ),
            )
        return

    # Otherwise, update the security in the portfolio.
    symbol, _, units, _, paid = result
    units = Decimal(units)
    paid = Decimal(paid)
    if type == "Buy":
        units += Decimal(amount / unit_price)
        paid += Decimal(amount)
    elif type == "Sell":
        units -= Decimal(amount / unit_price)
        paid -= Decimal(amount)
    # If the user has sold all of their units, remove the security from the
    # portfolio.
    if units == 0:
        # Delete the security from the portfolio.
        remove_security_from_portfolio(symbol)
    else:
        # Update the security in the portfolio
        with duckdb.connect(database=DB_PATH) as conn:
            conn.execute(
                "UPDATE portfolio SET units = ?, paid = ? WHERE symbol = ?",
                (str(units), str(paid), symbol),
            )


def remove_security_from_portfolio(symbol: str) -> None:
    """
    Remove the security from the portfolio table.

    Args:
        symbol: The symbol of the security.
    """
    with duckdb.connect(database=DB_PATH) as conn:
        conn.execute("DELETE FROM portfolio WHERE symbol = ?", (symbol,))

        
def get_total_paid_into_portfolio() -> Decimal:
    """
    Get the total amount paid into the portfolio.

    Returns:
        The total amount paid into the portfolio.
    """
    with duckdb.connect(database=DB_PATH) as conn:
        result = conn.execute(
            "SELECT SUM(CAST(paid AS DECIMAL)) FROM portfolio"
        ).fetchone()

    return Decimal(result[0]) if result else Decimal(0)

  
def get_exchange_rate(
    original_currency: str, convert_to: str = "GBP", provided_date: str = None
) -> Decimal:
    """
    Gets the exchange rate from a given currency
    to a given currency using Frankfurter API (https://www.frankfurter.app/).

    Args:
        original_currency: original currency to convert to given currency.
        convert_to: currency to convert to.
        provided_date: date to retrieve exchange rate from.

    Returns:
        Exchange rate from original currency -> given currency.
    """
    if original_currency == convert_to:
        return Decimal(1)

    url = None

    if not provided_date:
        # If no date is provided, the most recent exchange rate is retrieved.
        url = f"https://api.frankfurter.app/latest?from={original_currency}&to={convert_to}"
    else:
        # Checks to see if data is available for the date provided
        # Frankfurter API only provides exchange rate data since 4th January 1999.
        pdate = datetime.strptime(provided_date, "%Y-%m-%d").date()
        if pdate < date(1999, 1, 4):
            provided_date = "1999-01-04"

        url = f"https://api.frankfurter.app/{provided_date}?from={original_currency}&to={convert_to}"

    response = requests.get(url)
    data = response.json()
    return Decimal(data["rates"][convert_to])


if __name__ == "__main__":
    print(get_info("3697.T"))
    print(get_info("GSK.L"))

    print((get_exchange_rate("JPY", "GBP", "1998-04-04")))
