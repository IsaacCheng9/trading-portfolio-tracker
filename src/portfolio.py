"""
Handles the logic for the processing and storage of the user's trading
portfolio.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from decimal import Decimal

import duckdb
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import QTimer, QThread, QObject, Signal

from src.finance import get_absolute_rate_of_return, get_info
from src.transactions import AddTransactionDialog, TransactionHistoryDialog
from src.ui.main_window_ui import Ui_main_window

DB_PATH = "resources/portfolio.db"


class UpdateStockPricesWorker(QObject):
    finished = Signal()

    def __init__(self, interval, main_window):
        super().__init__()
        self.main_window = main_window
        self.interval = interval
        self.timer = QTimer()
        # Connects the timer timeout to the method to update stock prices
        self.timer.timeout.connect(self.update_stock_prices)

    def start_update(self) -> None:
        """
        Starts the loop to update stock prices
        at regular intervals.
        """
        self.timer.start(self.interval)

    def update_stock_prices(self) -> None:
        """
        Calls update stock prices from a thread and
        restarts timer.
        """
        self.main_window.update_stock_prices()
        # Restarts the timer if the timer is not active when method is called
        if not self.timer.isActive():
            self.timer.start()


class MainWindow(QMainWindow, Ui_main_window):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # Stores current information about each security (current price, change, abs rate of return)
        self.current_security_info = {}

        # Mapping between asset name and the row it occupies in the
        # portfolio table widget for updating purposes.
        self.portfolio_view_mapping = {}

        # Connect the 'Add Transaction' button to open the dialog.
        self.btn_add_transaction.clicked.connect(self.open_add_transaction_dialog)
        # Connect the 'View Transactions' button to open the dialog.
        self.btn_view_transactions.clicked.connect(self.open_transaction_history_dialog)

        # Set the resize mode of the table to resize the columns to fit
        # the contents by default.
        table_header = self.table_widget_portfolio.horizontalHeader()
        table_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.load_portfolio_table()

        # Calculates the interval for the refreshing of stock prices
        portfolio = HeldSecurity.load_portfolio()
        interval = None

        diff = 2000 - (2 * (60 * len(portfolio)))
        if diff > 0:
            interval = 6000
        else:
            # TODO Potentially improve dynamic calculation?
            diff = abs(diff)
            interval = 60000 + (diff * 1.1 * 60)

        # Creates a worker for the updating of stock prices
        self.worker = UpdateStockPricesWorker(interval, self)

        # Moves worker to a seperate thread
        self.thread = QThread()
        self.worker.moveToThread(self.thread)

        self.worker.finished.connect(self.thread.quit)
        self.thread.start()
        # Starts the update loop
        self.worker.start_update()

    def open_add_transaction_dialog(self) -> None:
        """
        Open the dialog to add a new transaction.
        """
        self.add_transaction_dialog = AddTransactionDialog()
        self.add_transaction_dialog.open()

    def open_transaction_history_dialog(self) -> None:
        """
        Open the dialog to view the user's transaction history.
        """
        self.transaction_history_dialog = TransactionHistoryDialog()
        self.transaction_history_dialog.open()

    def load_portfolio_table(self) -> None:
        """
        Load the user's portfolio into the table widget.
        """
        portfolio = HeldSecurity.load_portfolio()

        # Gets the current value, change in value, and rate of return of each security
        # and stores it in the current_security_info dictionary
        for security in portfolio:
            stock_info = get_info(security.name)
            cur_val = Decimal(stock_info["current_value"]) * security.units
            val_change = (
                Decimal(stock_info["current_value"]) - security.paid
            ) * security.units
            rate_of_return_abs = get_absolute_rate_of_return(
                Decimal(stock_info["current_value"]), security.paid
            )

            # Stores the live security information in a dictionary indexed
            # by the name of the security
            self.current_security_info[security.name] = (
                cur_val,
                val_change,
                rate_of_return_abs,
            )

        for n, security in enumerate(portfolio):
            self.table_widget_portfolio.insertRow(0)
            self.table_widget_portfolio.setItem(
                0, 0, QtWidgets.QTableWidgetItem(security.symbol)
            )
            self.table_widget_portfolio.setItem(
                0, 1, QtWidgets.QTableWidgetItem(security.name)
            )
            weight = str(
                round(
                    (
                        self.current_security_info[security.name][0]
                        / HeldSecurity.get_total_value(self.current_security_info)
                    )
                    * 100,
                    3,
                )
            )
            self.table_widget_portfolio.setItem(
                0, 2, QtWidgets.QTableWidgetItem(f"{weight}%")
            )
            self.table_widget_portfolio.setItem(
                0, 3, QtWidgets.QTableWidgetItem(str(security.units))
            )
            self.table_widget_portfolio.setItem(
                0, 4, QtWidgets.QTableWidgetItem(security.currency)
            )

            self.table_widget_portfolio.setItem(
                0,
                5,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][0]:.2f}"
                ),
            )
            self.table_widget_portfolio.setItem(
                0,
                6,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][1]:+.2f}"  # Change in value
                ),
            )
            self.table_widget_portfolio.setItem(
                0,
                7,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][2]:+.2f}%"
                ),
            )

            # Assigns the index in the portfolio view list of the security
            self.portfolio_view_mapping[security.name] = len(portfolio) - n - 1

        # Get the current time in DD/MM/YYYY HH:MM:SS format.
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_last_updated.setText(f"Last Updated: {cur_time}")

    def update_stock_prices(self) -> None:
        """
        Update live stock current prices, change in value, and
        absolute rate of return.
        """
        portfolio = HeldSecurity.load_portfolio()

        # Gets the current value, change in value, and rate of return of the current stock
        # and stores it in the current_security_info dictionary
        for security in portfolio:
            stock_info = get_info(security.name)

            cur_val = Decimal(stock_info["current_value"]) * security.units
            val_change = (
                Decimal(stock_info["current_value"]) - security.paid
            ) * security.units
            rate_of_return_abs = get_absolute_rate_of_return(
                Decimal(stock_info["current_value"]), security.paid
            )

            # Stores the live security information in a dictionary indexed
            # by the name of the security
            self.current_security_info[security.name] = (
                cur_val,
                val_change,
                rate_of_return_abs,
            )

        # Clear the table portfolio widget without clearing headers
        for row in range(self.table_widget_portfolio.rowCount()):
            for column in range(self.table_widget_portfolio.columnCount()):
                item = self.table_widget_portfolio.item(row, column)
                if item is not None:
                    self.table_widget_portfolio.takeItem(row, column)

        # Repopulate the table with the new data
        for security in portfolio:
            row = self.portfolio_view_mapping[security.name]
            self.table_widget_portfolio.setItem(
                row,
                1,
                QtWidgets.QTableWidgetItem(security.symbol),
            )
            self.table_widget_portfolio.setItem(
                row, 0, QtWidgets.QTableWidgetItem(security.name)
            )
            weight = str(
                round(
                    (
                        self.current_security_info[security.name][0]
                        / HeldSecurity.get_total_value(self.current_security_info)
                    )
                    * 100,
                    3,
                )
            )
            self.table_widget_portfolio.setItem(
                row, 2, QtWidgets.QTableWidgetItem(f"{weight}%")
            )
            self.table_widget_portfolio.setItem(
                row, 3, QtWidgets.QTableWidgetItem(str(security.units))
            )
            self.table_widget_portfolio.setItem(
                row, 4, QtWidgets.QTableWidgetItem(security.currency)
            )
            self.table_widget_portfolio.setItem(
                row,
                5,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][0]:.2f}"
                ),
            )
            self.table_widget_portfolio.setItem(
                row,
                6,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][1]:+.2f}"
                ),
            )
            self.table_widget_portfolio.setItem(
                row,
                7,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][2]:+.2f}%"
                ),
            )

        # Update last updated time label in dd-mm-yyyy hh:mm:ss format
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_last_updated.setText(f"Last Updated: {cur_time}")


@dataclass
class HeldSecurity:
    """
    Keep track of a security held by the user.
    """

    symbol: str
    name: str
    units: Decimal
    currency: str
    paid: Decimal

    @staticmethod
    def load_portfolio() -> list[HeldSecurity]:
        """
        Load the user's portfolio from DuckDB, containing details on each
        security they hold.

        Returns:
            A list of the securities and the details of each held by the user.
        """
        with duckdb.connect(database=DB_PATH) as conn:
            # Retrieve securities from the portfolio table
            result = conn.execute(
                "SELECT name, symbol, units, currency, paid FROM portfolio"
            )
            records = result.fetchall()

        # Create HeldSecurity objects for each record.
        portfolio = []
        for record in records:
            symbol, name, units, currency, paid = record
            # Convert the units and paid values to Decimal objects to avoid
            # floating point precision errors.
            units = Decimal(units)
            paid = Decimal(paid)
            security = HeldSecurity(name, symbol, units, currency, paid)
            portfolio.append(security)

        return portfolio

    @staticmethod
    def get_total_value(
        current_values: dict[str, tuple[Decimal, Decimal, Decimal]]
    ) -> Decimal:
        """
        Calculate the total current value of the user's portfolio.

        Returns:
            The total value of the portfolio.
        """
        total_value = Decimal(0)
        for key in current_values:
            total_value += current_values[key][0]

        return total_value


if __name__ == "__main__":
    with duckdb.connect(database=DB_PATH) as conn:
        # Create a table to store securities in the user's portfolio.
        conn.execute(
            "CREATE TABLE IF NOT EXISTS portfolio ("
            "symbol TEXT PRIMARY KEY, "
            "name TEXT NOT NULL, "
            "units TEXT NOT NULL, "
            "currency TEXT NOT NULL, "
            "paid TEXT NOT NULL"
            ")"
        )
        # # Load some mock data into the table.
        # conn.execute(
        #     "INSERT OR REPLACE INTO portfolio VALUES "
        #     "('AAPL', 'Apple Inc.', '10', 'USD', '1000'), "
        #     "('TSLA', 'Tesla Inc.', '5', 'USD', '3000'), "
        #     "('BTC', 'Bitcoin', '0.2', 'USD', '1000'),"
        #     "('HMC', 'Honda', '40', 'USD', '39.5'),"
        #     "('^IXIC', 'NASDAQ Composite', '10', 'USD', '10000'),"
        #     "('FTMC', 'FTSE 250', '2', 'GBP', '13520')"
        # )
    portfolio = HeldSecurity.load_portfolio()
