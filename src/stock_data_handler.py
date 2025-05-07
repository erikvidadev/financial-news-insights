import datetime

import pandas as pd
from pandas import DataFrame


class StockDataHandler:
    def __init__(self):
        self.csv_path: str = f"./data/processed/stock/stock_data_{datetime.datetime.now().strftime('%Y.%m.%d_%H.%M')}.csv"
        self.excel_path: str = f"./data/processed/stock/stock_data_{datetime.datetime.now().strftime('%Y.%m.%d_%H.%M')}.xlsx"

    def export_to_csv(self, df: DataFrame) -> bool:
        """
        Export dataframe to CSV format.

        Args:
            df (DataFrame): Pandas DataFrame containing stock data

        Returns:
            bool: True if export was successful, False otherwise

        Raises:
            IOError: If there's an issue writing to the specified path
        """
        try:
            df.to_csv(self.csv_path, index=False, encoding='utf-8')
            return True
        except Exception as e:
            raise IOError(f"Error exporting data to CSV at {self.csv_path}: {e}")

    def export_to_excel(self, df: DataFrame) -> bool:
        """
        Export dataframe to Excel format.

        Args:
            df (DataFrame): Pandas DataFrame containing stock data

        Returns:
            bool: True if export was successful, False otherwise

        Raises:
            IOError: If there's an issue writing to the specified path
        """
        try:
            df.to_excel(self.excel_path, index=False)
            return True
        except Exception as e:
            raise IOError(f"Error exporting data to Excel at {self.excel_path}: {e}")

    def export_to_all_formats(self, df: DataFrame) -> dict:
        """
        Export dataframe to all supported formats.

        Args:
            df (DataFrame): Pandas DataFrame containing stock data

        Returns:
            dict: Dictionary with format names as keys and export status as values
        """
        results = {}

        try:
            results['csv'] = self.export_to_csv(df)
        except IOError as e:
            results['csv'] = False

        try:
            results['excel'] = self.export_to_excel(df)
        except IOError as e:
            results['excel'] = False

        return results
