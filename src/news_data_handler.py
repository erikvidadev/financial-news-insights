import datetime
import json
import os
from typing import Any, Dict, Optional, List, Union

import pandas as pd


class NewsDataHandler:
    def __init__(self):
        self.raw_input_path: str = f"./data/raw/news/raw_articles.json"
        self.csv_output_path: str = f"./data/processed/news/articles.csv"
        self.excel_output_path: str = f"./data/processed/news/articles.xlsx"

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
        if not isinstance(data_to_save, (dict, list)):
            raise TypeError("Data to save must be a dictionary or list of dictionaries")
        if isinstance(data_to_save, list) and not all(isinstance(item, dict) for item in data_to_save):
            raise TypeError("All items in the list must be dictionaries")

        try:
            os.makedirs(os.path.dirname(self.raw_input_path), exist_ok=True)

            with open(self.raw_input_path, "w", encoding="utf-8") as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)

            return self.raw_input_path

        except (IOError, OSError) as e:
            raise IOError(f"Failed to save data to {self.raw_input_path}: {str(e)}")
        except TypeError as e:
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
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Handle if data is a dict with 'articles' or just a list of articles
            if isinstance(data, dict):
                articles = data.get('articles', [])
            elif isinstance(data, list):
                articles = data
            else:
                raise TypeError("Unexpected data format: Expected dict or list")

            if not articles:
                return pd.DataFrame()

            articles_dataframe = pd.DataFrame(articles)

            # Handle nested 'source' field if exists
            if 'source' in articles_dataframe.columns:
                articles_dataframe['source_name'] = articles_dataframe['source'].apply(
                    lambda x: x.get('name') if isinstance(x, dict) else None
                )
                articles_dataframe = articles_dataframe.drop('source', axis=1)

            return articles_dataframe

        except (json.JSONDecodeError, TypeError) as e:
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
        if formats is None:
            formats = ['csv', 'excel']

        results = {}

        for format_type in formats:
            if format_type.lower() == 'csv':
                results['csv'] = self._export_to_csv(df)
            elif format_type.lower() == 'excel':
                results['excel'] = self._export_to_excel(df)
            else:
                raise ValueError(f"Unsupported export format: {format_type}")

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
            os.makedirs(os.path.dirname(self.csv_output_path), exist_ok=True)
            articles_dataframe.to_csv(self.csv_output_path, index=False, encoding='utf-8')
            return True
        except Exception as e:
            print(f"Error exporting to CSV {self.csv_output_path}: {e}")
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
            os.makedirs(os.path.dirname(self.excel_output_path), exist_ok=True)
            articles_dataframe.to_excel(self.excel_output_path, index=False)
            return True
        except Exception as e:
            print(f"Error exporting to Excel {self.excel_output_path}: {e}")
            return False
