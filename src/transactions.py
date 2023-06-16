"""
Handles the logic for the processing and storage of the user's trading
transactions.
"""
from __future__ import annotations

import datetime
import time
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID, uuid4

import duckdb
from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog

from src.ui.add_transaction_ui import Ui_dialog_add_transaction
from src.ui.transaction_history_ui import Ui_dialog_transaction_history

DB_PATH = "resources/portfolio.db"


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
        transactions = Transaction.load_transaction_history()
        for transaction in transactions:
            self.table_widget_transactions.insertRow(0)
            self.table_widget_transactions.setItem(
                0, 0, QtWidgets.QTableWidgetItem(transaction.type)
            )
            self.table_widget_transactions.setItem(
                0, 1, QtWidgets.QTableWidgetItem(str(transaction.timestamp))
            )
            self.table_widget_transactions.setItem(
                0, 2, QtWidgets.QTableWidgetItem(str(transaction.id))
            )
            self.table_widget_transactions.setItem(
                0, 3, QtWidgets.QTableWidgetItem(str(transaction.symbol))
            )
            # TODO: Get the name of the security from the symbol using yfinance.
            self.table_widget_transactions.setItem(
                0, 5, QtWidgets.QTableWidgetItem(str(transaction.platform))
            )
            self.table_widget_transactions.setItem(
                0, 6, QtWidgets.QTableWidgetItem(str(transaction.currency))
            )
            self.table_widget_transactions.setItem(
                0, 7, QtWidgets.QTableWidgetItem(str(transaction.amount))
            )
            self.table_widget_transactions.setItem(
                0, 8, QtWidgets.QTableWidgetItem(str(transaction.unit_price))
            )

        # Get the current time in DD/MM/YYYY HH:MM:SS format.
        cur_time = time.strftime("%d/%m/%Y %H:%M:%S")
        self.lbl_last_updated.setText(f"Last Updated: {cur_time}")


class AddTransactionDialog(QDialog, Ui_dialog_add_transaction):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

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
        # Ensure that the ticker only contains letters.
        if not self.line_edit_symbol.text().isalpha():
            self.lbl_status_msg.setText("The ticker can only contain letters.")
            return
        # Ensure that the amount and unit price are positive.
        if (
            float(self.line_edit_amount.text()) <= 0.0
            or float(self.line_edit_unit_price.text()) <= 0.0
        ):
            self.lbl_status_msg.setText("The amount and unit price must be positive.")
            return

        # Create a new transaction object and save it to the database.
        new_transaction = Transaction(
            uuid4(),
            self.combo_box_transaction_type.currentText(),
            self.datetime_edit_transaction.dateTime().toPython(),
            self.line_edit_symbol.text().upper(),
            self.line_edit_platform.text(),
            self.line_edit_currency.text(),
            Decimal(self.line_edit_amount.text()),
            Decimal(self.line_edit_unit_price.text()),
        )
        new_transaction.save()
        self.close()


@dataclass
class Transaction:
    id: UUID
    type: str
    timestamp: datetime.datetime
    symbol: str
    platform: str
    currency: str
    amount: Decimal
    unit_price: Decimal

    @staticmethod
    def load_transaction_history() -> list[Transaction]:
        """
        Load the user's transactions from DuckDB.

        Returns:
            A list of the user's transactions, sorted by timestamp.
        """
        with duckdb.connect(database=DB_PATH) as conn:
            # Load the transactions from the database.
            records = conn.execute(
                """
                SELECT *
                FROM transaction
                ORDER BY timestamp DESC
                """
            ).fetchall()

        # Create Transaction objects for each record.
        transactions = []
        for record in records:
            (
                transaction_id,
                transaction_type,
                timestamp,
                ticker,
                platform,
                currency,
                amount,
                unit_price,
            ) = record
            # Convert timestamp to remove the milliseconds.
            timestamp = datetime.datetime.strptime(
                str(timestamp), "%Y-%m-%d %H:%M:%S.%f"
            ).replace(microsecond=0)
            # Convert the amount and unit price to Decimal objects to avoid
            # floating point precision errors.
            amount = Decimal(amount)
            unit_price = Decimal(unit_price)
            transaction = Transaction(
                transaction_id,
                transaction_type,
                timestamp,
                ticker,
                platform,
                currency,
                amount,
                unit_price,
            )
            transactions.append(transaction)

        return transactions

    def save(self) -> None:
        """
        Add a record to the transaction table.
        """
        with duckdb.connect(database=DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO transaction VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.id,
                    self.type,
                    self.timestamp,
                    self.symbol,
                    self.platform,
                    self.currency,
                    str(self.amount),
                    str(self.unit_price),
                ),
            )


if __name__ == "__main__":
    with duckdb.connect(database=DB_PATH) as conn:
        # Create a table to store the transactions made by the user.
        conn.execute(
            "CREATE TABLE IF NOT EXISTS transaction ("
            "transaction_id TEXT PRIMARY KEY, "
            "transaction_type TEXT NOT NULL, "
            "timestamp DATETIME NOT NULL, "
            "ticker TEXT NOT NULL, "
            "platform TEXT NOT NULL, "
            "currency TEXT NOT NULL, "
            "amount TEXT NOT NULL, "
            "unit_price TEXT NOT NULL"
            ")"
        )
