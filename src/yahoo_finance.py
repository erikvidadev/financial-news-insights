import pandas as pd
import yfinance as yf


class YahooFinanceClient:
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

    def get_stock_data(self) -> pd.DataFrame:
        """
        Fetch stock data for the specified symbol, period, and interval.

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

