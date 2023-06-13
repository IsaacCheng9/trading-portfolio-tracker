"""
Handles the logic for the processing and storage of the user's trading
transactions.
"""
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDialog
from PySide6.QtCore import QDateTime

from src.ui.add_transaction_ui import Ui_dialog_add_transaction


class AddTransactionDialog(QDialog):
    def __init__(self) -> None:
        super().__init__()
        self.ui = Ui_dialog_add_transaction()
        self.ui.setupUi(self)

        # Set the datetime edit to the current date and time.
        self.ui.datetime_edit_transaction.setDateTime(QDateTime.currentDateTime())
        # Ensure that the value field only accepts up to two decimal places.
        self.ui.line_edit_value.setValidator(QDoubleValidator(decimals=2))

        # Connect the 'Submit' button to create a new transaction.
        self.ui.btn_submit_transaction.clicked.connect(self.add_transaction)
        # Close the dialog when the 'Cancel' button is clicked.
        self.ui.btn_cancel_transaction.clicked.connect(self.close)

    def add_transaction(self) -> None:
        """
        Add a new transaction to the database.
        """
        pass
