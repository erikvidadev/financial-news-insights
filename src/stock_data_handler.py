import logging
from pandas import DataFrame

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StockDataHandler:
    def __init__(self):
        self.csv_path: str = f"./data/processed/stock_data.csv"
        self.excel_path: str = f"./data/processed/stock_data.xlsx"
        logger.info(f"StockDataHandler initialized with CSV path {self.csv_path} and Excel path {self.excel_path}")

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
        logger.info(f"Exporting data to CSV at {self}")
        try:
            df.to_csv(self.csv_path, index=False, encoding='utf-8')
            logger.info("Successfully exported data to CSV")
            return True
        except Exception as e:
            logger.error(f"Error exporting data to CSV: {e}")
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
        logger.info(f"Exporting data to Excel at {self.excel_path}")
        try:
            df.to_excel(self.excel_path, index=False)
            logger.info("Successfully exported data to Excel")
            return True
        except Exception as e:
            logger.error(f"Error exporting data to Excel {e}")
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

        logger.info("Starting export to all formats")
        try:
            results['csv'] = self.export_to_csv(df)
        except IOError as e:
            logger.warning(f"CSV export failed: {e}")
            results['csv'] = False

        """try:
            results['excel'] = self.export_to_excel(df)
        except IOError as e:
            logger.warning(f"Excel export failed: {e}")
            results['excel'] = False"""

        logger.info(f"Export results: {results}")
        return results
