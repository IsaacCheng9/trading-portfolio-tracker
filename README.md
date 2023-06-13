# Trading Portfolio Tracker

[![code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![CI](https://github.com/IsaacCheng9/trading-portfolio-tracker/actions/workflows/pytest.yml/badge.svg)

A platform for monitoring and managing your investment portfolios with real-time
market data integration from Yahoo Finance, developed with Qt.

## Usage

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
