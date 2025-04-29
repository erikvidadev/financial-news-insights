from typing import Dict, Any, List
import json

import requests
from dotenv import load_dotenv
import os
from requests import Response


class NewsApiClient:
    """Client for fetching news articles from the News API."""

    def __init__(
            self,
            search_query: str,
            start_date: str,
            end_date: str,
    ) -> None:
        """
        Initialize the News API client.

        Args:
            source_domains: The domain to fetch news from
            search_query: The keyword to search for in news articles
            categories: List of news categories to filter by
            start_date: The beginning of the search
            end_date: The end date of the search
        """
        load_dotenv()
        self._api_key = os.getenv("NEWS_API_KEY")
        self.endpoint = "https://newsapi.org/v2/everything"
        self.search_query = search_query
        self.start_date = start_date
        self.end_date = end_date

    def fetch_articles(self) -> Response:
        """
        Fetch news articles based on the configured parameters.

        Returns:
            Response: The HTTP response from the News API
        """
        url = (
            f'{self.endpoint}'
            f'?q={self.search_query}'
            f'&from={self.start_date}'
            f'&to={self.end_date}'
            f'&apiKey={self._api_key}'
        )
        print(url)
        return requests.get(url)

    def get_articles(self) -> Dict[str, Any]:
        """
        Fetch articles and return them as a dictionary.

        Returns:
            Dict[str, Any]: The parsed JSON response as a dictionary,
                           or an error dictionary if the request failed
        """
        response = self.fetch_articles()

        if response.status_code == 200:
            return response.json()
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }

    def save_response_json(self, filename: str = None) -> None:
        """
        Save the JSON response from the News API to a file in the data/raw/ directory.

        Args:
            filename (str): The name of the file to save the response to.
                                      If not provided, a default name will be used.
        """
        articles = self.get_articles()
        if not filename:
            filename = f"data/raw/news/news_response_{self.start_date}_{self.end_date}.json"

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)