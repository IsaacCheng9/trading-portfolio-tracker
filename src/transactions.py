"""
Handles the logic for the processing and storage of the user's trading
transactions.
"""
import datetime
from uuid import uuid4
from dataclasses import dataclass
from decimal import Decimal

import duckdb
from PySide6.QtCore import QDateTime
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog

from src.ui.add_transaction_ui import Ui_dialog_add_transaction

DB_PATH = "resources/portfolio.db"


class AddTransactionDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_dialog_add_transaction()
        self.ui.setupUi(self)

        # Set the datetime edit to the current date and time.
        self.ui.datetime_edit_transaction.setDateTime(QDateTime.currentDateTime())
        # Ensure that the amount field only accepts up to two decimal places.
        self.ui.line_edit_amount.setValidator(QDoubleValidator(decimals=2))

        # Connect the 'Submit' button to create a new transaction.
        self.ui.btn_submit_transaction.clicked.connect(self.add_transaction)
        # Close the dialog when the 'Cancel' button is clicked.
        self.ui.btn_cancel_transaction.clicked.connect(self.close)

    def add_transaction(self) -> None:
        """
        Add a new transaction to the database.
        """
        pass


@dataclass
class Transaction:
    transaction_id: uuid4
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
                    uuid4(),
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
            "ticker TEXT, "
            "platform TEXT, "
            "currency TEXT, "
            "amount TEXT, "
            "unit_price TEXT"
            ")"
        )
