from datetime import datetime, timedelta
from typing import Dict, Any, Union, Optional, List
from readability import Document
from lxml import html

import requests
from dotenv import load_dotenv
import os
from requests import Response


class NewsApiClient:
    """Client for fetching news articles from the News API."""

    def __init__(
            self,
            search_query: str,
            categories: Union[str, List[str]],
            search_days: int,
            api_key: Optional[str] = None,
    ) -> None:
        """
        Initialize the News API client.

        Args:
            search_query: The keyword to search for in news articles
            categories: Category or list of news categories to filter by
            search_days: Number of days in the past to search for articles
            api_key: Optional API key. If not provided, will be loaded from environment
        """
        if api_key:
            self._api_key = api_key
        else:
            load_dotenv()
            self._api_key = os.getenv("NEWS_API_KEY")

        if not self._api_key:
            raise ValueError("API key not provided and NEWS_API_KEY not found in environment")

        self.endpoint = "https://newsapi.org/v2/everything"
        self.search_query = search_query
        self.categories = categories
        self.end_date = self._get_end_date()
        self.start_date = self._get_start_date(search_days)
        self.language: str =  "en"

    def fetch_articles(self) -> Response:
        """
        Fetch news articles based on the configured parameters.

        Returns:
            Response: The HTTP response from the News API
        """
        url = (
            f'{self.endpoint}'
            f'?q={self.search_query}'
            f'&categories={self.categories}'
            f'&language={self.language}'
            f'&from={self.start_date}'
            f'&to={self._get_end_date()}'
            f'&apiKey={self._api_key}'
        )
        return requests.get(url)

    def _get_start_date(self, days_from_now: int) -> str:
        """
        Calculate the start date for the search period.

        Args:
            days_from_now: Number of days in the past

        Returns:
            Formatted date string in YYYY-MM-DD format
        """
        start_date = datetime.today() - timedelta(days=days_from_now)
        return start_date.strftime('%Y-%m-%d')

    def _get_end_date(self) -> str:
        """
        Get the current date as the end date for the search period.

        Returns:
            Formatted date string in YYYY-MM-DD format
        """
        return datetime.today().strftime('%Y-%m-%d')

    def get_articles(self) -> Dict[str, Any]:
        """
        Fetch articles and return them as a dictionary.

        Returns:
            Dict[str, Any]: The parsed JSON response as a dictionary,
                          or an error dictionary if the request failed
        """
        try:
            response = self.fetch_articles()

            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": True,
                    "status_code": response.status_code,
                    "message": response.text
                }
        except requests.RequestException as e:
            return {
                "error": True,
                "exception": str(e),
                "message": "Network error occurred"
            }
        except ValueError as e:
            return {
                "error": True,
                "exception": str(e),
                "message": "Failed to parse response"
            }

    def extract_full_articles(self, ) -> List[Dict[str, Any]]:
        """
        Given a list of articles (from NewsAPI), fetch and extract full article content using readability.

        Returns:
            List[Dict[str, Any]]: List of articles with full text added (under key 'full_text')
        """
        articles = self.get_articles().get("articles", [])

        full_articles = []

        for article in articles:
            article_url = article.get("url")
            if not article_url:
                continue

            try:
                response = requests.get(article_url, timeout=10)
                response.raise_for_status()
                content_html = Document(response.text).summary()
                content_text = html.fromstring(content_html).text_content()

                article['full_text'] = content_text.strip()
                full_articles.append(article)

            except Exception as e:
                article['full_text'] = f"[Error fetching content: {e}]"
                full_articles.append(article)

        return full_articles



