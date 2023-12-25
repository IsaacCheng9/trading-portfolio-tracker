"""
Import the DuckDB database schema and data from a directory where it was
previously exported by a user. This is preferred over version controlling the
DB file itself due to merge conflicts and other issues that arise with binary
files.
"""
import duckdb

# The directory to import the DB file from.
import_from = "resources/portfolio_data"
# The directory to load the DB into.
import_to = "resources/portfolio.db"

conn = duckdb.connect(import_to)
conn.execute(f"IMPORT DATABASE '{import_from}'")
