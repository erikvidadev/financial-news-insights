import json
import os
import logging
from typing import Any, Dict, Optional, List, Union

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NewsDataHandler:
    def __init__(self):
        self.raw_output_path: str = f"./data/raw/raw_articles.json"
        self.processed_csv_output_path: str = f"./data/processed/articles.csv"
        self._processed_excel_output_path: str = f"./data/processed/articles.xlsx"

    def save_raw_data(self, data_to_save: Union[Dict[str, Any], List[Dict[str, Any]]]) -> str:
        """
        Save the JSON response from the News API to a file.

        Args:
            data_to_save (Union[Dict[str, Any], List[Dict[str, Any]]]): The JSON data to save.

        Returns:
            str: The name of the file where the data was saved.

        Raises:
            IOError: If there is an error writing to the file.
            TypeError: If the data cannot be serialized to JSON.
        """
        logger.info("Saving raw data to JSON file.")
        if not isinstance(data_to_save, (dict, list)):
            logger.error("Invalid data type for saving: expected dict or list.")
            raise TypeError("Data to save must be a dictionary or list of dictionaries")
        if isinstance(data_to_save, list) and not all(isinstance(item, dict) for item in data_to_save):
            logger.error("Invalid list format: all items must be dictionaries.")
            raise TypeError("All items in the list must be dictionaries")

        try:
            os.makedirs(os.path.dirname(self.raw_output_path), exist_ok=True)
            with open(self.raw_output_path, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
            logger.info(f"Successfully saved raw data to {self.raw_output_path}")
            return self.raw_output_path

        except (IOError, OSError) as e:
            logger.exception(f"Failed to save data to {self.raw_output_path}")
            raise IOError(f"Failed to save data to {self.raw_output_path}: {str(e)}")
        except TypeError as e:
            logger.exception("Failed to serialize data to JSON")
            raise TypeError(f"Failed to serialize data to JSON: {str(e)}")

    def process_raw_data(self, file_path: str) -> pd.DataFrame:
        """
        Read a JSON file containing news data and convert it to a pandas DataFrame.

        Args:
            file_path: Path to the JSON file containing news data.

        Returns:
            DataFrame containing the processed news articles.

        Raises:
            FileNotFoundError: If the specified file does not exist.
            json.JSONDecodeError: If the file does not contain valid JSON.
            RuntimeError: If there's any other error processing the data.
        """
        logger.info(f"Processing raw data from file: {file_path}")
        if not os.path.isfile(file_path):
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            logger.info("Successfully loaded JSON data.")

            if isinstance(data, dict):
                articles = data.get('articles', [])
            elif isinstance(data, list):
                articles = data
            else:
                logger.error("Unexpected JSON structure: expected dict or list.")
                raise TypeError("Unexpected data format: Expected dict or list")

            if not articles:
                logger.warning("No articles found in data.")
                return pd.DataFrame()

            articles_dataframe = pd.DataFrame(articles)

            if 'source' in articles_dataframe.columns:
                articles_dataframe['source_name'] = articles_dataframe['source'].apply(
                    lambda x: x.get('name') if isinstance(x, dict) else None
                )
                articles_dataframe = articles_dataframe.drop('source', axis=1)

            logger.info(f"Processed {len(articles_dataframe)} articles into DataFrame.")
            return articles_dataframe

        except (json.JSONDecodeError, TypeError) as e:
            logger.exception("Failed to process JSON data.")
            raise RuntimeError(f"Error processing news data: {str(e)}")

    def export_articles(self, df: pd.DataFrame, formats: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Export dataframe to specified formats.

        Args:
            df: DataFrame to export.
            formats: List of formats to export to. Defaults to ['csv', 'excel'] if None.
                     Valid values are 'csv' and 'excel'.

        Returns:
            Dictionary with format names as keys and success status as values.

        Raises:
            ValueError: If an invalid format is specified.
        """
        logger.info("Exporting articles to formats.")
        if formats is None:
            formats = ['csv']  # Add 'excel' if needed

        results = {}

        for format_type in formats:
            if format_type.lower() == 'csv':
                results['csv'] = self._export_to_csv(df)
            elif format_type.lower() == 'excel':
                results['excel'] = self._export_to_excel(df)
            else:
                logger.error(f"Unsupported format specified: {format_type}")
                raise ValueError(f"Unsupported export format: {format_type}")

        logger.info(f"Export results: {results}")
        return results

    def _export_to_csv(self, articles_dataframe: pd.DataFrame) -> bool:
        """
        Export dataframe to CSV format.

        Args:
            articles_dataframe: DataFrame to export.

        Returns:
            True if export was successful, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(self.processed_csv_output_path), exist_ok=True)
            articles_dataframe.to_csv(self.processed_csv_output_path, index=False, encoding='utf-8')
            logger.info(f"Data exported to CSV at: {self.processed_csv_output_path}")
            return True
        except Exception as e:
            logger.exception(f"Error exporting to CSV: {self.processed_csv_output_path}")
            print(f"Error exporting to CSV {self.processed_csv_output_path}: {e}")
            return False

    def _export_to_excel(self, articles_dataframe: pd.DataFrame) -> bool:
        """
        Export dataframe to Excel format.

        Args:
            articles_dataframe: DataFrame to export.

        Returns:
            True if export was successful, False otherwise.
        """
        try:
            os.makedirs(os.path.dirname(self._processed_excel_output_path), exist_ok=True)
            articles_dataframe.to_excel(self._processed_excel_output_path, index=False)
            logger.info(f"Data exported to Excel at: {self._processed_excel_output_path}")
            return True
        except Exception as e:
            logger.exception(f"Error exporting to Excel: {self._processed_excel_output_path}")
            print(f"Error exporting to Excel {self._processed_excel_output_path}: {e}")
            return False
