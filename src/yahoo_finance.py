import pandas as pd
import yfinance as yf
from typing import List, Optional


class YahooFinanceClient:
    """
    A client to fetch stock data from Yahoo Finance using the yfinance library.

    Attributes:
        stock_symbol (str): The ticker symbol for the stock (e.g., 'AAPL' for Apple Inc.)
        period (str): The time period to retrieve data for (e.g., '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'max')
        interval (str): The data interval (e.g., '1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo')
    """

    # Valid options for period and interval parameters
    VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
    VALID_INTERVALS = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

    def __init__(self, stock_symbol: str, period: str = '1mo', interval: str = '1d') -> None:
        """
        Initialize the YahooFinanceClient object.

        Args:
            stock_symbol (str): The ticker symbol for the stock
            period (str, optional): The time period to retrieve data for. Defaults to '1mo'.
            interval (str, optional): The data interval. Defaults to '1d'.

        Raises:
            ValueError: If the provided period or interval is not valid
        """
        self.stock_symbol: str = stock_symbol

        # Validate period and interval
        if period not in self.VALID_PERIODS:
            raise ValueError(f"Invalid period: {period}. Must be one of {self.VALID_PERIODS}")
        if interval not in self.VALID_INTERVALS:
            raise ValueError(f"Invalid interval: {interval}. Must be one of {self.VALID_INTERVALS}")

        self.period: str = period
        self.interval: str = interval

    def fetch_stock_data(self) -> pd.DataFrame:
        """
        Fetch stock data for the specified symbol, period, and interval from Yahoo Finance.

        Returns:
            pd.DataFrame: A pandas DataFrame containing the stock data with columns for
                         Open, High, Low, Close, Adj Close, and Volume

        Raises:
            ValueError: If the stock symbol is invalid or no data is found
            ConnectionError: If there's a network issue connecting to Yahoo Finance
            Exception: For any other unexpected errors
        """
        try:
            # Note: yfinance.download always returns a pandas DataFrame
            stock_data: pd.DataFrame = yf.download(
                tickers=self.stock_symbol,
                period=self.period,
                interval=self.interval,
                progress=False  # Disable progress bar for cleaner output
            )

            if stock_data.empty:
                raise ValueError(f"No data found for symbol: {self.stock_symbol}")

            return stock_data

        except ValueError as e:
            raise ValueError(f"Value Error: {e}")
        except ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Yahoo Finance: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching stock data: {str(e)}")

    def fetch_multiple_stocks(self, symbols: List[str]) -> pd.DataFrame:
        """
        Fetch data for multiple stock symbols using the same period and interval.

        Args:
            symbols (List[str]): List of ticker symbols to fetch

        Returns:
            pd.DataFrame: A pandas DataFrame containing data for all requested symbols

        Raises:
            ValueError: If any symbol is invalid or no data is found
            ConnectionError: If there's a network issue connecting to Yahoo Finance
        """
        try:
            # Join symbols with space for yfinance
            tickers = " ".join(symbols)

            # Download data for multiple tickers
            stock_data: pd.DataFrame = yf.download(
                tickers=tickers,
                period=self.period,
                interval=self.interval,
                group_by='ticker',  # Group columns by ticker
                progress=False  # Disable progress bar
            )

            if stock_data.empty:
                raise ValueError(f"No data found for symbols: {symbols}")

            return stock_data

        except ValueError as e:
            raise ValueError(f"Value Error: {e}")
        except ConnectionError as e:
            raise ConnectionError(f"Failed to connect to Yahoo Finance: {str(e)}")
        except Exception as e:
            raise Exception(f"Error fetching stock data: {str(e)}")