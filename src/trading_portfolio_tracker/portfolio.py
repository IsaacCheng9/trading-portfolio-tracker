"""
Handles the logic for the processing and storage of the user's trading
portfolio.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from decimal import Decimal
from uuid import uuid4

import duckdb
from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime, QObject, QThread, QTimer, Signal
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog, QMainWindow

from src.trading_portfolio_tracker.finance import (
    get_exchange_rate,
    get_info,
    get_name_from_symbol,
    get_rate_of_return,
    get_total_paid_into_portfolio,
    upsert_transaction_into_portfolio,
)
from src.trading_portfolio_tracker.transactions import Transaction
from src.trading_portfolio_tracker.ui.add_transaction_ui import (
    Ui_dialog_add_transaction,
)
from src.trading_portfolio_tracker.ui.main_window_ui import Ui_main_window
from src.trading_portfolio_tracker.ui.portfolio_performance_ui import (
    Ui_dialog_portfolio_perf,
)
from src.trading_portfolio_tracker.ui.transaction_history_ui import (
    Ui_dialog_transaction_history,
)

DB_PATH = "resources/portfolio.duckdb"


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
        self.portfolio_perf_dialog = None
        self.add_transaction_dialog = None
        self.transaction_history_dialog = None
        self.setupUi(self)

        # Stores current information about each security:
        # (current price, change, abs rate of return, price in GBP)
        self.current_security_info = {}

        # Mapping between asset name and the row it occupies in the
        # portfolio table widget for updating purposes.
        self.portfolio_view_mapping = {}

        # Connect the 'Add Transaction' button to open the dialog.
        self.btn_add_transaction.clicked.connect(self.open_add_transaction_dialog)
        # Connect the 'View Transactions' button to open the dialog.
        self.btn_view_transactions.clicked.connect(self.open_transaction_history_dialog)
        # Connect the 'Analyse Portfolio Performance' button.
        self.btn_view_portfolio_perf.clicked.connect(self.open_portfolio_perf_dialog)

        # Set the resize mode of the table to resize the columns to fit
        # the contents by default.
        returns_table_header = self.table_widget_returns.horizontalHeader()
        returns_table_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        portfolio_table_header = self.table_widget_portfolio.horizontalHeader()
        portfolio_table_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        # Resize the returns table to fit one row.
        self.table_widget_returns.setFixedHeight(
            self.table_widget_returns.rowHeight(0)
            + self.table_widget_returns.horizontalHeader().height()
            + 2
        )

        # Calculates the interval for the refreshing of stock prices
        self.load_portfolio_table()
        self.update_returns_table()
        portfolio = HeldSecurity.load_portfolio()

        diff = 2000 - (2 * (60 * len(portfolio)))
        if diff > 0:
            interval = 6000
        else:
            # TODO Potentially improve dynamic calculation? See 'Smarter scraping' section: https://pypi.org/project/yfinance/
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
        self.add_transaction_dialog = AddTransactionDialog(self)
        self.add_transaction_dialog.open()

    def open_transaction_history_dialog(self) -> None:
        """
        Open the dialog to view the user's transaction history.
        """
        self.transaction_history_dialog = TransactionHistoryDialog()
        self.transaction_history_dialog.open()

    def open_portfolio_perf_dialog(self) -> None:
        """
        Open the dialog to view the user's portfolio performance analysis.
        """
        self.portfolio_perf_dialog = PortfolioPerfDialog()
        self.portfolio_perf_dialog.open()

    def update_returns_table(self) -> None:
        """
        Update the table of returns based on the latest prices.
        """
        portfolio = HeldSecurity.load_portfolio()
        self.get_pricing_data_for_securities(portfolio)
        total_paid = get_total_paid_into_portfolio()
        # Sum the current value and value change for all securities in the
        # portfolio.
        total_cur_val = Decimal(
            sum(self.current_security_info[security.name][3] for security in portfolio)
        )
        total_val_change = Decimal(
            sum(self.current_security_info[security.name][1] for security in portfolio)
        )
        rate_of_return_absolute = get_rate_of_return(total_cur_val, total_paid)

        # Update the table with the new values.
        self.table_widget_returns.setItem(
            0, 0, QtWidgets.QTableWidgetItem(f"{total_paid:.2f}")
        )
        self.table_widget_returns.setItem(
            0, 1, QtWidgets.QTableWidgetItem(f"{total_cur_val:.2f}")
        )
        self.table_widget_returns.setItem(
            0, 2, QtWidgets.QTableWidgetItem(f"{total_val_change:.2f}")
        )
        self.table_widget_returns.setItem(
            0, 3, QtWidgets.QTableWidgetItem(f"{rate_of_return_absolute:.3f}%")
        )
        # TODO: Add time-weighted rate of return metric.

    def load_portfolio_table(self) -> None:
        """
        Load the user's portfolio into the table widget.
        """
        portfolio = HeldSecurity.load_portfolio()
        self.get_pricing_data_for_securities(portfolio)
        # Clear all rows except the header row.
        self.table_widget_portfolio.setRowCount(0)

        for row, security in enumerate(portfolio):
            (
                cur_val,
                val_change,
                rate_of_return_abs,
                cur_val_gbp,
            ) = self.current_security_info[security.name]
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
                        self.current_security_info[security.name][3]
                        / HeldSecurity.get_total_value(self.current_security_info, True)
                    )
                    * 100,
                    3,
                )
            )
            self.table_widget_portfolio.setItem(
                0, 2, QtWidgets.QTableWidgetItem(f"{weight}%")
            )
            self.table_widget_portfolio.setItem(
                0, 3, QtWidgets.QTableWidgetItem(security.currency)
            )
            # Round the units to 5 DP to prevent horizontal stretching.
            units = round(security.units, 5)
            self.table_widget_portfolio.setItem(
                0, 4, QtWidgets.QTableWidgetItem(str(units))
            )

            self.table_widget_portfolio.setItem(
                0,
                5,
                QtWidgets.QTableWidgetItem(f"{(cur_val / security.units):.2f}"),
            )
            self.table_widget_portfolio.setItem(
                0,
                6,
                QtWidgets.QTableWidgetItem(f"{cur_val_gbp:.2f}"),
            )
            self.table_widget_portfolio.setItem(
                0,
                7,
                QtWidgets.QTableWidgetItem(f"{val_change:+.2f}"),
            )
            self.table_widget_portfolio.setItem(
                0,
                8,
                QtWidgets.QTableWidgetItem(f"{rate_of_return_abs:+.2f}%"),
            )

            # Assigns the index in the portfolio view list of the security
            self.portfolio_view_mapping[security.name] = len(portfolio) - row - 1

        # Get the current time in DD/MM/YYYY HH:MM:SS format.
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_last_updated.setText(f"Last Updated: {cur_time}")

    def get_pricing_data_for_securities(self, portfolio: list[HeldSecurity]) -> None:
        """
        Get the current value, change in value, and rate of return (absolute)
        for each security in the portfolio.

        Args:
            portfolio: A list of HeldSecurity objects.
        """
        for security in portfolio:
            stock_info = get_info(security.symbol)

            cur_val = Decimal(stock_info["current_value"]) * security.units
            exchange_rate = get_exchange_rate(stock_info["currency"])
            cur_val_gbp = cur_val * exchange_rate

            val_change = cur_val_gbp - security.paid_gbp
            rate_of_return_abs = get_rate_of_return(cur_val_gbp, security.paid_gbp)

            # Stores the live security information in a dictionary indexed
            # by the name of the security
            self.current_security_info[security.name] = (
                cur_val,
                val_change,
                rate_of_return_abs,
                cur_val_gbp,
            )

    def update_stock_prices(self) -> None:
        """
        Update live stock current prices, change in value, and
        absolute rate of return.

        # TODO: Avoid code duplication by using load_portfolio_table() instead.
        """
        portfolio = HeldSecurity.load_portfolio()
        self.get_pricing_data_for_securities(portfolio)

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
                0,
                QtWidgets.QTableWidgetItem(security.symbol),
            )
            self.table_widget_portfolio.setItem(
                row, 1, QtWidgets.QTableWidgetItem(security.name)
            )
            weight = str(
                round(
                    (
                        self.current_security_info[security.name][3]
                        / HeldSecurity.get_total_value(self.current_security_info, True)
                    )
                    * 100,
                    3,
                )
            )
            self.table_widget_portfolio.setItem(
                row, 2, QtWidgets.QTableWidgetItem(f"{weight}%")
            )
            self.table_widget_portfolio.setItem(
                row, 3, QtWidgets.QTableWidgetItem(security.currency)
            )
            # Round units to 5 DP to prevent horizontal stretching.
            units = round(security.units, 5)
            self.table_widget_portfolio.setItem(
                row, 4, QtWidgets.QTableWidgetItem(str(units))
            )
            self.table_widget_portfolio.setItem(
                row,
                5,
                QtWidgets.QTableWidgetItem(
                    f"{(self.current_security_info[security.name][0] / security.units):.2f}"
                ),
            )
            # Value (GBP)
            self.table_widget_portfolio.setItem(
                row,
                6,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][3]:.2f}"
                ),
            )
            # Change (GBP)
            self.table_widget_portfolio.setItem(
                row,
                7,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][1]:+.2f}"
                ),
            )
            # Rate of Return (Absolute)
            self.table_widget_portfolio.setItem(
                row,
                8,
                QtWidgets.QTableWidgetItem(
                    f"{self.current_security_info[security.name][2]:+.3f}%"
                ),
            )

        self.update_returns_table()
        # Update last updated time label in dd-mm-yyyy hh:mm:ss format
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_last_updated.setText(f"Last Updated: {cur_time}")


class PortfolioPerfDialog(QDialog, Ui_dialog_portfolio_perf):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # Set the resize mode of the table to resize the columns to fit
        # the contents by default.
        table_header = self.table_widget_returns_breakdown.horizontalHeader()
        table_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )

        self.update_returns_breakdown()

    def update_returns_breakdown(self):
        """
        Update the breakdown of returns for the user's portfolio.
        """
        portfolio = HeldSecurity.load_portfolio()
        total_cur_val = Decimal(0.0)
        total_cur_val_gbp = Decimal(0.0)
        total_paid = Decimal(0.0)
        total_paid_gbp = Decimal(0.0)

        # Calculate the cumulative total paid and current value of the
        # portfolio.
        for security in portfolio:
            stock_info = get_info(security.symbol)
            cur_val = Decimal(stock_info["current_value"]) * security.units
            total_cur_val += cur_val
            total_paid += security.paid
            total_paid_gbp += security.paid_gbp
            exchange_rate = get_exchange_rate(stock_info["currency"])
            total_cur_val_gbp += cur_val * exchange_rate

        # Absolute rate of return
        rate_of_return_absolute = get_rate_of_return(total_cur_val_gbp, total_paid_gbp)
        self.table_widget_returns_breakdown.setItem(
            0, 0, QtWidgets.QTableWidgetItem(f"{rate_of_return_absolute:.3f}%")
        )
        # Return from change in value
        val_change_return = get_rate_of_return(total_cur_val, total_paid)
        self.table_widget_returns_breakdown.setItem(
            0, 1, QtWidgets.QTableWidgetItem(f"{val_change_return:.3f}%")
        )
        # Return from currency risk
        # Currency risk is the returns caused by fluctuations in the exchange
        # rate between the currency of the security and GBP since the
        # security was purchased. If the GBP has weakened against the original
        # currency, it results in a positive return, and vice versa.
        currency_risk_return = rate_of_return_absolute - val_change_return
        self.table_widget_returns_breakdown.setItem(
            0, 2, QtWidgets.QTableWidgetItem(f"{currency_risk_return:.3f}%")
        )

        # Get the current time in DD/MM/YYYY HH:MM:SS format.
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_last_updated.setText(f"Last Updated: {cur_time}")


class TransactionHistoryDialog(QDialog, Ui_dialog_transaction_history):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # Set the resize mode of the table to resize the columns to fit
        # the contents by default.
        table_header = self.table_widget_transactions.horizontalHeader()
        table_header.setSectionResizeMode(
            QtWidgets.QHeaderView.ResizeMode.ResizeToContents
        )
        self.load_transaction_history_table()

    def load_transaction_history_table(self) -> None:
        """
        Load the user's transaction history into the table.
        """
        transactions = Transaction.load_transaction_history()
        for transaction in transactions:
            # Round these values to prevent horizontally stretching the table.
            amount = round(Decimal(transaction.amount), 2)
            amount_gbp = round(Decimal(transaction.amount_gbp), 2)
            unit_price = round(Decimal(transaction.unit_price), 5)
            units = round(Decimal(transaction.units), 5)
            exchange_rate = round(Decimal(transaction.exchange_rate), 5)

            self.table_widget_transactions.insertRow(0)
            self.table_widget_transactions.setItem(
                0, 0, QtWidgets.QTableWidgetItem(transaction.type)
            )
            self.table_widget_transactions.setItem(
                0, 1, QtWidgets.QTableWidgetItem(str(transaction.timestamp))
            )
            self.table_widget_transactions.setItem(
                0, 2, QtWidgets.QTableWidgetItem(str(transaction.symbol))
            )
            self.table_widget_transactions.setItem(
                0,
                3,
                QtWidgets.QTableWidgetItem(get_name_from_symbol(transaction.symbol)),
            )
            self.table_widget_transactions.setItem(
                0, 4, QtWidgets.QTableWidgetItem(str(transaction.platform))
            )
            self.table_widget_transactions.setItem(
                0, 5, QtWidgets.QTableWidgetItem(str(transaction.currency))
            )
            self.table_widget_transactions.setItem(
                0, 6, QtWidgets.QTableWidgetItem(str(amount))
            )
            self.table_widget_transactions.setItem(
                0,
                7,
                QtWidgets.QTableWidgetItem(str(amount_gbp)),
            )
            self.table_widget_transactions.setItem(
                0, 8, QtWidgets.QTableWidgetItem(str(unit_price))
            )
            self.table_widget_transactions.setItem(
                0, 9, QtWidgets.QTableWidgetItem(str(units))
            )
            self.table_widget_transactions.setItem(
                0, 10, QtWidgets.QTableWidgetItem(str(exchange_rate))
            )
            self.table_widget_transactions.setItem(
                0, 11, QtWidgets.QTableWidgetItem(str(transaction.id))
            )

        # Get the current time in DD/MM/YYYY HH:MM:SS format.
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_last_updated.setText(f"Last Updated: {cur_time}")


class AddTransactionDialog(QDialog, Ui_dialog_add_transaction):
    def __init__(self, main_window_instance) -> None:
        super().__init__()
        self.setupUi(self)
        self.main_window = main_window_instance

        # Set the datetime edit to the current date and time.
        self.datetime_edit_transaction.setDateTime(QDateTime.currentDateTime())
        # Ensure that the amount field only accepts up to two decimal places.
        self.line_edit_amount.setValidator(QDoubleValidator(decimals=2))
        # Ensure that the unit price field only accepts up to two decimal places.
        self.line_edit_unit_price.setValidator(QDoubleValidator(decimals=2))

        # Connect the 'Submit' button to create a new transaction.
        self.btn_submit_transaction.clicked.connect(self.add_transaction)
        # Close the dialog when the 'Cancel' button is clicked.
        self.btn_cancel_transaction.clicked.connect(self.close)

    def add_transaction(self) -> None:
        """
        Add a new transaction to the database if it's valid.
        """
        # Ensure that none of the fields are empty.
        if (
            not self.combo_box_transaction_type.currentText()
            or not self.line_edit_symbol.text()
            or not self.line_edit_platform.text()
            or not self.line_edit_currency.text()
            or not self.line_edit_amount.text()
            or not self.line_edit_unit_price.text()
        ):
            self.lbl_status_msg.setText("Please fill in all of the details.")
            return
        # Ensure that the timestamp isn't in the future.
        if self.datetime_edit_transaction.dateTime() > QDateTime.currentDateTime():
            self.lbl_status_msg.setText(
                "The transaction timestamp cannot be in the future."
            )
            return
        # Ensure that the ticker exists.
        if not get_name_from_symbol(self.line_edit_symbol.text().upper()):
            self.lbl_status_msg.setText("The ticker symbol is invalid.")
            return
        # Ensure that the amount and unit price are positive.
        if (
            float(self.line_edit_amount.text()) <= 0.0
            or float(self.line_edit_unit_price.text()) <= 0.0
        ):
            self.lbl_status_msg.setText("The amount and unit price must be positive.")
            return

        # Extract the transaction details from the form.
        transaction_type = self.combo_box_transaction_type.currentText()
        timestamp = self.datetime_edit_transaction.dateTime().toPython()
        symbol = self.line_edit_symbol.text().upper()
        platform = self.line_edit_platform.text()
        currency = self.line_edit_currency.text()
        amount = Decimal(self.line_edit_amount.text())
        unit_price = Decimal(self.line_edit_unit_price.text())

        # Check if the stock is traded on the LSE.
        # if so, modify the currency from GBX to GBP.
        if symbol[-2:] == ".L":
            unit_price *= Decimal(0.01)

        units = Decimal(amount / unit_price)
        exchange_rate = get_exchange_rate(currency, provided_date=str(timestamp.date()))
        paid_gbp = amount * exchange_rate

        # Create a new transaction object and save it to the database.
        new_transaction = Transaction(
            uuid4(),
            transaction_type,
            timestamp,
            symbol,
            platform,
            currency,
            amount,
            unit_price,
            units,
            paid_gbp,
            exchange_rate,
        )
        new_transaction.save()
        upsert_transaction_into_portfolio(
            transaction_type, symbol, currency, amount, unit_price, paid_gbp
        )
        self.main_window.load_portfolio_table()
        self.main_window.update_returns_table()
        self.close()


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
    paid_gbp: Decimal

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
                "SELECT symbol, name, units, currency, paid, paid_gbp FROM portfolio"
            )
            records = result.fetchall()

        # Create HeldSecurity objects for each record.
        portfolio = []
        for record in records:
            symbol, name, units, currency, paid, paid_gbp = record
            # Convert the units and paid values to Decimal objects to avoid
            # floating point precision errors.
            units = Decimal(units)
            paid = Decimal(paid)
            paid_gbp = Decimal(paid_gbp)
            security = HeldSecurity(symbol, name, units, currency, paid, paid_gbp)
            portfolio.append(security)

        return portfolio

    @staticmethod
    def get_total_value(
        current_values: dict[str, tuple[Decimal, Decimal, Decimal]],
        is_gbp: bool = False,
    ) -> Decimal:
        """
        Calculate the total current value of the user's portfolio.

        Args:
            current_values: Current stock values.
            is_gbp: If total value of the user's portfolio should be calculated
                    in a standard currency (GBP).

        Returns:
            The total value of the portfolio.
        """
        cur_vals_key = 3 if is_gbp else 0
        total_value = Decimal(0)
        for key in current_values:
            total_value += current_values[key][cur_vals_key]

        return total_value


if __name__ == "__main__":
    print(HeldSecurity.load_portfolio())
