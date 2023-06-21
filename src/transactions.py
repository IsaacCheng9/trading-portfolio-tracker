"""
Handles the logic for the processing and storage of the user's trading
transactions.
"""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

import duckdb

DB_PATH = "resources/portfolio.db"


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
    units: Decimal
    paid_standard_currency: Decimal

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
                units,
                paid_standard_currency,
            ) = record
            # Convert timestamp to remove the milliseconds.
            timestamp = datetime.datetime.strptime(
                str(timestamp), "%Y-%m-%d %H:%M:%S.%f"
            ).replace(microsecond=0)
            # Convert to Decimal objects to avoid floating point precision
            # errors.
            amount = Decimal(amount)
            unit_price = Decimal(unit_price)
            units = Decimal(units)
            transaction = Transaction(
                transaction_id,
                transaction_type,
                timestamp,
                ticker,
                platform,
                currency,
                amount,
                unit_price,
                units,
                paid_standard_currency,
            )
            transactions.append(transaction)

        return transactions

    def save(self) -> None:
        """
        Add a record to the transaction table.
        """
        with duckdb.connect(database=DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO transaction VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.id,
                    self.type,
                    self.timestamp,
                    self.symbol,
                    self.platform,
                    self.currency,
                    str(self.amount),
                    str(self.unit_price),
                    str(self.units),
                    str(self.paid_standard_currency),
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
            "unit_price TEXT NOT NULL,"
            "units TEXT NOT NULL,"
            "paid_standard_currency TEXT NOT NULL"
            ")"
        )
