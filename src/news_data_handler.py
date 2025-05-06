import datetime
import json
import os
from pathlib import Path
from typing import Any

import pandas as pd
from pandas import DataFrame


class NewsDataHandler:
    def __init__(self):
        self.file_name: str = f"data/raw/news/news_response_{datetime.datetime.today()}.json"
        self.csv_output: str = f"./data/processed/news/news_articles.csv"
        self.excel_output: str = f"./data/processed/news/news_articles.xlsx"

    def save_raw_data(self, file_to_save: dict[str, Any]) -> str:
        """
        Save the JSON response from the News API to a file in the data/raw/ directory.

        Args:
            file_to_save (dict[str, Any]): The JSON data to save.

        Returns:
            str: The name of the file where the data was saved.
        """

        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)

        with open(self.file_name, "w", encoding="utf-8") as f:
            json.dump(file_to_save, f, ensure_ascii=False, indent=4)

        return self.file_name


    def process_raw_data(self, file_name: str):
        """
          Read a JSON file containing news data and convert it to a pandas DataFrame.

          Parameters:
          file_path (str): Path to the JSON file

          Returns:
          pandas.DataFrame: DataFrame containing the news articles
          """


        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Extract articles and create DataFrame
        articles = data.get('articles', [])
        df = pd.DataFrame(articles)

        # Handle nested source column (if exists)
        if 'source' in df.columns:
            df['source_name'] = df['source'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
            df = df.drop('source', axis=1)

        return df

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
            print(self.excel_output)
            print(f"Error exporting data: {e}")
            return False
