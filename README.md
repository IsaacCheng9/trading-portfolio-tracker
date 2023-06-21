# Trading Portfolio Tracker

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![CI](https://github.com/IsaacCheng9/trading-portfolio-tracker/actions/workflows/pytest.yml/badge.svg)

A cross-platform desktop application for monitoring and managing your investments
from different brokers, with real-time market data integration from Yahoo
Finance, developed with Qt.

## Motivation

Managing investments across different brokers can be challenging, as existing
broker-specific systems such as Trading 212 often limit users to viewing
investments exclusively within their own platforms. This leads to scattered
investment information and a lack of holistic oversight. While some users
resort to manual data entry in spreadsheets, this approach lacks real-time
market data and user-friendliness.

This application offers a centralised solution for monitoring and managing
investments across different brokers. By providing real-time market data
integration and a user-friendly interface, it enhances the investment management
experience. Additionally, as a desktop application, it prioritises data privacy
by storing all information locally on the user's computer. Leveraging the Qt
framework ensures cross-platform compatibility and high performance.

## Usage

### Operating System

Compatible with:

- macOS
- Windows
- Linux

### Python Version

We have developed and tested this application to work on Python 3.8 onwards.

### Running the Application

To run the application, you should follow the following steps from the
[root](./) directory:

1. Install the required Python libraries: `pip install -r requirements.txt`
2. Run the application with the command: `python -m src.app`

### Running the Tests

The tests are written using the [pytest](https://docs.pytest.org/en/stable/)
library. Ensure that you have the correct version installed by running the
following command from the [root](./) directory:

```bash
pip install -r requirements.txt
```

To run the tests, use the following command from the [tests](tests/) directory:

```bash
pytest
```

## Data Privacy

We store all data locally on the user's computer in a
DuckDB database at [/resources/portfolio.db](./resources/portfolio.db). Live
market data is fetched from Yahoo Finance, but we do not store any of this data
permanently.
