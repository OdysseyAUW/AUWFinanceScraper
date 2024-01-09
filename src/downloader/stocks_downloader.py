import requests
import os
from typing import Union, List
from pathlib import Path
from pandas import DataFrame
from .rate_limiter import RateLimiter
from .models import Stock
from ..utils.file_utils import create_dir
from ..config.settings import API_KEY
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

FORMATS = ["csv", "json", "parquet", "feather", "pickle"]

class StocksDownloader:
    """
    StocksDownloader class will return historical stock data on a daily interval for a given list of tickers.
    """
    def __init__(self, threads: int = 1, progress: bool = False, fpath: str = './data/stocks', override: bool = False, rate_limit_per_minute: int = 300, api_key: None | str = None) -> None:
        self.threads = threads
        self.progress = progress
        self.fpath = Path(fpath)
        self.override = override
        self.rate_limit_per_minute = rate_limit_per_minute
        self.start_date = "2000-01-01"
        self.url = "https://financialmodelingprep.com/api/v3/historical-price-full/"
        self.tickers = []
        self.failures = []
        self.rate_limiter = RateLimiter(self.rate_limit_per_minute, 60)
        if api_key is None: raise ValueError("api_key must be provided. Please contact dmbernaal@gmail.com for information")
        create_dir(self.fpath)

    def __repr__(self) -> str:
        return f"StocksDownloader(threads={self.threads}, progress={self.progress}, fpath={self.fpath}, override={self.override}, rate_limit_per_minute={self.rate_limit_per_minute}, start_date={self.start_date}, url={self.url}, tickers={self.tickers}, failures={self.failures})"

    def _format_tickers(self, tickers: Union[str, List[str]]) -> None:
        if not isinstance(tickers, list) and not isinstance(tickers, str):
            raise ValueError("tickers must be a list of strings or a string separated by commas")
        if isinstance(tickers, str): tickers = tickers.replace(",", " ").split()
        self.tickers = tickers

    def _save(self, data: Stock, ticker: str, format: str) -> None:
        if format not in FORMATS: raise ValueError(f"format must be one of {FORMATS}")
        folder = f"{self.fpath}/{ticker}"
        create_dir(folder)
        fpath = f"{folder}/{ticker}_price_{data.first}_TO_{data.last}.{format}"
        if os.path.exists(fpath) and not self.override: 
            print(f"File {fpath} already exists. Skipping...")
            return
        if format == "csv": data.data.to_csv(fpath, index=False)
        elif format == "json": data.data.to_json(fpath, orient="records")
        elif format == "parquet": data.data.to_parquet(fpath, index=False)
        elif format == "feather": data.data.to_feather(fpath)
        elif format == "pickle": data.data.to_pickle(fpath)
    
    def _download(self, ticker: str) -> Stock | None:
        self.rate_limiter.wait()
        try:
            response = requests.get(f"{self.url}{ticker}?from={self.start_date}&apikey={API_KEY}")
            if response.status_code != 200: 
                self.failures.append(ticker)
                raise Exception(f"Error: {response.status_code}")
            self.rate_limiter.add_call()
            data = response.json()
            if not data: 
                self.failures.append(ticker)
                return None
            last = data["historical"][0]["date"]
            first = data["historical"][-1]["date"]
            obj = {'data': DataFrame(data["historical"]), "first": first, "last": last}
            return Stock(**obj)
        except Exception as e:
            print(f"Error: {e}")
            self.failures.append(ticker)
            return None
        
    def _download_and_save(self, ticker: str, format: str) -> None:
        data = self._download(ticker)
        if data: self._save(data, ticker, format)

    def from_text(self, fpath: str, format: str = "csv") -> None:
        with open(fpath, "r") as f:
            tickers = f.read().replace(",", " ").split()
            self.get(tickers, format)
    
    def get(self, tickers: Union[str, List[str]], format: str = "csv") -> None:
        self._format_tickers(tickers)
        with ThreadPoolExecutor(max_workers=self.threads) as executor, tqdm(total=len(self.tickers)) as progress:
            futures = {executor.submit(self._download_and_save, ticker, format): ticker for ticker in self.tickers}
            for future in as_completed(futures):
                ticker = futures[future]
                progress.update(1)
                progress.set_description(f"Processing {ticker}")
        print(f"Downloaded {len(self.tickers) - len(self.failures)} out of {len(self.tickers)} tickers. To view failures, call .failures")