import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf


class StockData:
    """
      A class to fetch stock data using the yfinance library.

      Attributes:
          stock_symbol (str): The ticker symbol for the stock (e.g., 'AAPL' for Apple Inc.)
          period (str): The time period to retrieve data for (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
          interval (str): The data interval (e.g., '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
      """

    def __init__(self, stock_symbol: str, period: str, interval: str) -> None:
        """
        Initialize the StockData object.

        Args:
            stock_symbol (str): The ticker symbol for the stock
            period (str): The time period to retrieve data for
            interval (str): The data interval
        """
        self.stock_symbol: str = stock_symbol
        self.period: str = period
        self.interval: str = interval

    def fetch_stock_data(self) -> pd.DataFrame:
        """
        Fetch stock data for the specified symbol, period, and interval.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the stock data with columns for
                         Open, High, Low, Close, Adj Close, and Volume
        """
        # Note: yfinance.download always returns a pandas DataFrame
        stock_data: pd.DataFrame = yf.download(
            tickers=self.stock_symbol,
            period=self.period,
            interval=self.interval
        )
        print(stock_data)
        return stock_data

    def save_stock_data_to_files(self, output_dir: str = "data/processed/stock") -> None:
        """
        Saves fetched stock data to CSV and Excel files in the specified directory.

        :param output_dir:
        Directory path where the output files will be saved.
        Default is "data/processed/stock".
        """
        data = self.fetch_stock_data()

        # Remove timezone info from datetime index
        data.index = data.index.tz_localize(None)

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Format base filename
        today_str = datetime.datetime.today().strftime("%Y-%m-%d")
        base_filename = f"{self.stock_symbol}_{self.period}_{self.interval}_{today_str}"

        # Define full paths
        csv_path = Path(output_dir) / f"{base_filename}.csv"
        excel_path = Path(output_dir) / f"{base_filename}.xlsx"

        # Save to files
        data.to_csv(csv_path)
        data.to_excel(excel_path)




