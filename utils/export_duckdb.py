"""
Export the DuckDB database schema and data to a directory to be imported later
by the user. This is preferred over version controlling the DB file itself
due to merge conflicts and other issues that arise with binary files.
"""
import duckdb

# The directory to get the DB file from.
export_from = "resources/portfolio.db"
# The directory to export the DB to.
export_to = "resources/portfolio_data"

conn = duckdb.connect(export_from)
conn.execute(f"EXPORT DATABASE '{export_to}'")
