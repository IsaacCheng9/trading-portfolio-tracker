COPY "transaction" FROM 'resources/portfolio_data/transaction.csv' (FORMAT 'csv', quote '"', delimiter ',', header 1);
COPY portfolio FROM 'resources/portfolio_data/portfolio.csv' (FORMAT 'csv', quote '"', delimiter ',', header 1);
