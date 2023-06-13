"""
Handles the logic for the processing and storage of the user's trading
portfolio.
"""

from dataclasses import dataclass
from decimal import Decimal
import time
import duckdb
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow

from src.ui.main_window_ui import Ui_main_window

DB_PATH = "resources/portfolio.db"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # Set the resize mode of the table to resize the columns to fit
        # the contents by default.
        table_header = self.ui.table_widget_portfolio.horizontalHeader()
        table_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.load_portfolio_table()

    def load_portfolio_table(self):
        """
        Load the user's portfolio into the table widget.
        """
        portfolio = HeldSecurity.load_portfolio()
        for security in portfolio:
            self.ui.table_widget_portfolio.insertRow(0)
            self.ui.table_widget_portfolio.setItem(
                0, 1, QtWidgets.QTableWidgetItem(security.ticker)
            )
            self.ui.table_widget_portfolio.setItem(
                0, 0, QtWidgets.QTableWidgetItem(security.name)
            )
            self.ui.table_widget_portfolio.setItem(
                0, 3, QtWidgets.QTableWidgetItem(str(security.units))
            )
            self.ui.table_widget_portfolio.setItem(
                0, 4, QtWidgets.QTableWidgetItem(security.currency)
            )
            self.ui.table_widget_portfolio.setItem(
                0, 5, QtWidgets.QTableWidgetItem(str(security.paid))
            )

        # Get the current time in DD/MM/YYYY HH:MM:SS format.
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.ui.lbl_last_updated.setText(f"Last Updated: {cur_time}")


@dataclass
class HeldSecurity:
    """
    Keep track of a security held by the user.
    """

    ticker: str
    name: str
    units: Decimal
    currency: str
    paid: Decimal

    def save(self):
        with duckdb.connect(database=DB_PATH) as conn:
            # Insert or update the security in the portfolio table.
            conn.execute(
                "INSERT OR REPLACE INTO portfolio VALUES (?, ?, ?, ?, ?)",
                (
                    self.ticker,
                    self.name,
                    str(self.units),
                    self.currency,
                    str(self.paid),
                ),
            )

    @staticmethod
    def load_portfolio():
        with duckdb.connect(database=DB_PATH) as conn:
            # Retrieve securities from the portfolio table
            result = conn.execute(
                "SELECT name, ticker, units, currency, paid FROM portfolio"
            )
            records = result.fetchall()

        # Create HeldSecurity objects for each record.
        portfolio = []
        for record in records:
            name, ticker, units, currency, paid = record
            # Convert the units and paid values to Decimal objects to avoid
            # floating point precision errors.
            units = Decimal(units)
            paid = Decimal(paid)
            security = HeldSecurity(name, ticker, units, currency, paid)
            portfolio.append(security)

        return portfolio

    @staticmethod
    def print_portfolio(portfolio):
        portfolio = HeldSecurity.load_portfolio()
        for security in portfolio:
            print(security)


if __name__ == "__main__":
    with duckdb.connect(database=DB_PATH) as conn:
        # Create a table to store portfolio information
        conn.execute(
            "CREATE TABLE IF NOT EXISTS portfolio ("
            "ticker TEXT PRIMARY KEY, "
            "name TEXT, "
            "units TEXT, "
            "currency TEXT, "
            "paid TEXT"
            ")"
        )
        # Load some mock data into the table.
        conn.execute(
            "INSERT OR REPLACE INTO portfolio VALUES "
            "('AAPL', 'Apple Inc.', '10', 'USD', '1000'), "
            "('TSLA', 'Tesla Inc.', '5', 'USD', '3000'), "
            "('BTC', 'Bitcoin', '0.2', 'USD', '1000')"
        )
    portfolio = HeldSecurity.load_portfolio()
    HeldSecurity.print_portfolio(portfolio)
