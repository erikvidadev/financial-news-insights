import datetime

import pandas as pd
from pandas import DataFrame


class StockDataHandler:
    def __init__(self):
        self.csv_output: str = f"./data/processed/stock/APPLE_stock_data.csv"
        self.excel_output: str = f"./data/processed/stock/APPLE_stock_data.xlsx"

    def export_to_csv(self, df: DataFrame):
        """Export dataframe to CSV formats."""
        try:
            df.to_csv(self.csv_output, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(self.csv_output)
            print(f"Error exporting data: {e}")
            return False

    def export_to_excel(self, df: DataFrame):
        """Export dataframe to EXCEL formats."""
        try:
            df.to_excel(self.excel_output, index=False)
            return True
        except Exception as e:
            print(self.csv_output)
            print(f"Error exporting data: {e}")
            return False

