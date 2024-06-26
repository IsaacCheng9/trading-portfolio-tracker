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

DB_PATH = "resources/portfolio.duckdb"


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
    amount_gbp: Decimal
    exchange_rate: Decimal

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
                amount_gbp,
                exchange_rate,
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
                amount_gbp,
                exchange_rate,
            )
            transactions.append(transaction)

        return transactions

    def save(self) -> None:
        """
        Add a record to the transaction table.
        """
        with duckdb.connect(database=DB_PATH) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO transaction "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
                    str(self.amount_gbp),
                    str(self.exchange_rate),
                ),
            )


if __name__ == "__main__":
    print(Transaction.load_transaction_history())
