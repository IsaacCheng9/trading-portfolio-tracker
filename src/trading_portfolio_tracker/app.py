import duckdb
import sys
import os
from PySide6 import QtWidgets
from src.trading_portfolio_tracker.portfolio import MainWindow

DB_PATH = "resources/portfolio.db"


def main() -> None:
    """
    Open the main menu on program startup.
    """
    # Create the database tables if they don't already exist.
    create_database_tables()
    # No scaling is required - increase font sizes instead if necessary.
    os.environ["QT_SCALE_FACTOR"] = "1"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_menu = MainWindow()
    main_menu.show()
    sys.exit(app.exec())


def create_database_tables(database_path: str = DB_PATH) -> None:
    """
    Create the database tables if they don't already exist.
    """
    # Create a table to store securities in the user's portfolio.
    with duckdb.connect(database=database_path) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS portfolio ("
            "symbol TEXT PRIMARY KEY, "
            "name TEXT NOT NULL, "
            "units TEXT NOT NULL, "
            "currency TEXT NOT NULL, "
            "paid TEXT NOT NULL,"
            "paid_gbp TEXT NOT NULL"
            ")"
        )

    # Create a table to store the transactions made by the user.
    with duckdb.connect(database=database_path) as conn:
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
            "amount_gbp TEXT NOT NULL,"
            "exchange_rate TEXT NOT NULL"
            ")"
        )


if __name__ == "__main__":
    main()
