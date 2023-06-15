"""
Handles the logic for the processing and storage of the user's trading
transactions.
"""
import datetime
from uuid import UUID, uuid4
from dataclasses import dataclass
from decimal import Decimal

import duckdb
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog

from src.ui.add_transaction_ui import Ui_dialog_add_transaction

DB_PATH = "resources/portfolio.db"


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
            or not self.line_edit_ticker.text()
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
        if not self.line_edit_ticker.text().isalpha():
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
            self.line_edit_ticker.text().upper(),
            self.line_edit_platform.text(),
            self.line_edit_currency.text(),
            self.line_edit_amount.text(),
            self.line_edit_unit_price.text(),
        )
        new_transaction.save()
        self.close()


@dataclass
class Transaction:
    transaction_id: UUID
    transaction_type: str
    timestamp: datetime
    ticker: str
    platform: str
    currency: str
    amount: Decimal
    unit_price: Decimal

    def save(self) -> None:
        """
        Add a record to the transaction table.
        """
        with duckdb.connect(database=DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO transaction VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.transaction_id,
                    self.transaction_type,
                    self.timestamp,
                    self.ticker,
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
