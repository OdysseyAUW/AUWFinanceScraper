# AUW Finance Stock Data

This framework is a Python tool for downloading historical stock data. It supports various data formats and offers features like rate limiting and parallel data processing.

In the future we will include bulk-downloads including fundamental data.

**Active Development**
This project is in active development and many improvements must be made. Currently, we only support a few exchanges so one of the next features will require ```(TICKER, EXCHANGE)``` pairs to appropriately map a downloader.

## Installation

To install this framework, follow these steps:

1. **Clone the Repository**:
2. **CD Into Project**
3. **Install the Package**:
Ideally, create a python environment if not a conda env to install the packages
```
pip install -e .
```

## Usage

The framework can be used in Python scripts or Jupyter notebooks.

## 1. Local Array
```python
from src.downloader.stocks_downloader import StocksDownloader

# instantiate the downloader
downloader = StocksDownloader(
    threads=4, # number of threads to use for downloading
    progress=True, # show progress bar
    fpath='./data/stocks/', # path to save the data
    rate_limit_per_minute=300, # rate limit per minute DEFAULT for API
    api_key=API_KEY # API key
)

tickers = ["ATNF", "NMTRQ", "ABT", "ATGE", "AFRM", "ABNB", "ALIT", "ARLP", "GOOGL", "ALPP", "ALPSQ", "ASPS"]

# download the data
# you can change the format to: csv, json, parquet, feather, pickle
# for simplicity we will use csv
downloader.get(tickers, format='csv')
```

## 2. .txt file
```python
from src.downloader.stocks_downloader import StocksDownloader

# instantiate the downloader
downloader = StocksDownloader(
    threads=4, # number of threads to use for downloading
    progress=True, # show progress bar
    fpath='./data/stocks/', # path to save the data
    rate_limit_per_minute=300, # rate limit per minute DEFAULT for API
    api_key=API_KEY # API key
)

# download the data
downloader.from_text('test_stocks.txt', format='csv')
```