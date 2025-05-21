from datetime import datetime, timedelta
from typing import Dict, Any, Union, Optional, List
from readability import Document
from lxml import html
import logging
import requests
from dotenv import load_dotenv
import os
from requests import Response

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsApiError(Exception):
    """Custom exception for News API related errors."""
    pass


class NewsApiClient:
    """Client for fetching news articles from the News API."""

    def __init__(
            self,
            search_query: str,
            categories: Union[str, List[str]],
            search_days: int,
            api_key: Optional[str] = None,
            log_level: int = logging.INFO
    ) -> None:
        """
        Initialize the News API client.

        Args:
            search_query: The keyword to search for in news articles
            categories: Category or list of categories to filter by
            search_days: Number of days in the past to search for articles
            api_key: Optional API key. If not provided, will be loaded from environment
            log_level: Logging level (default: logging.INFO)
        """
        logger.info(f"Initializing NewsApiClient with query: '{search_query}'")

        if api_key:
            self._api_key = api_key
            logger.debug("Using provided API key")
        else:
            logger.debug("No API key provided, attempting to load from environment")
            load_dotenv()
            self._api_key = os.getenv("NEWS_API_KEY")

        if not self._api_key:
            logger.error("API key not found in environment and not provided")
            raise NewsApiError("API key not provided and NEWS_API_KEY not found in environment")

        self.endpoint = "https://newsapi.org/v2/everything"
        self.search_query = search_query

        if isinstance(categories, list):
            self.categories = ",".join(categories)
            logger.debug(f"Categories converted from list to string: {self.categories}")
        else:
            self.categories = categories

        self.end_date = self._get_end_date()
        self.start_date = self._get_start_date(search_days)
        self.language: str = "en"

        logger.info(f"NewsApiClient initialized for date range: {self.start_date} to {self.end_date}")

    def fetch_articles(self) -> Response:
        """
        Fetch news articles based on the configured parameters.

        Returns:
            Response: The HTTP response from the News API

        Raises:
            requests.RequestException: If there's a network error
            NewsApiError: If the API returns an error
        """
        url = (
            f'{self.endpoint}'
            f'?q={self.search_query}'
            f'&categories={self.categories}'
            f'&language={self.language}'
            f'&from={self.start_date}'
            f'&to={self.end_date}'
            f'&apiKey={self._api_key}'
        )

        safe_url = url.replace(self._api_key, "API_KEY_REDACTED")
        logger.debug(f"Making request to: {safe_url}")

        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info(f"API request successful: {response.status_code}")
            return response
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            if response.status_code == 401:
                logger.error("Authentication error - check your API key")
                raise NewsApiError("Authentication failed - invalid API key") from e
            elif response.status_code == 429:
                logger.error("Rate limit exceeded")
                raise NewsApiError("Rate limit exceeded - try again later") from e
            else:
                logger.error(f"API error: {response.text}")
                raise NewsApiError(f"API returned error {response.status_code}: {response.text}") from e
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise NewsApiError("Connection error - check your internet connection") from e
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {e}")
            raise NewsApiError("Request timed out - the server might be slow or unavailable") from e
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {e}")
            raise NewsApiError(f"Request failed: {str(e)}") from e

    def _get_start_date(self, days_from_now: int) -> str:
        """
        Calculate the start date for the search period.

        Args:
            days_from_now: Number of days in the past

        Returns:
            Formatted date string in YYYY-MM-DD format
        """
        start_date = datetime.today() - timedelta(days=days_from_now)
        result = start_date.strftime('%Y-%m-%d')
        logger.debug(f"Calculated start date: {result}")
        return result

    def _get_end_date(self) -> str:
        """
        Get the current date as the end date for the search period.

        Returns:
            Formatted date string in YYYY-MM-DD format
        """
        result = datetime.today().strftime('%Y-%m-%d')
        logger.debug(f"Calculated end date: {result}")
        return result

    def get_articles(self) -> Dict[str, Any]:
        """
        Fetch articles and return them as a dictionary.

        Returns:
            Dict[str, Any]: The parsed JSON response as a dictionary

        Raises:
            NewsApiError: If the API request fails or returns an error
        """
        try:
            logger.info(f"Fetching articles for query: '{self.search_query}'")
            response = self.fetch_articles()
            data = response.json()

            if "status" in data and data["status"] == "error":
                logger.error(f"API returned error: {data.get('message', 'Unknown error')}")
                raise NewsApiError(f"News API error: {data.get('message', 'Unknown error')}")

            article_count = len(data.get("articles", []))
            logger.info(f"Successfully fetched {article_count} articles")
            return data
        except NewsApiError:
            raise
        except requests.exceptions.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {e}")
            raise NewsApiError("Failed to parse API response") from e
        except Exception as e:
            logger.error(f"Unexpected error in get_articles: {e}", exc_info=True)
            raise NewsApiError(f"Unexpected error: {str(e)}") from e

    def extract_full_articles(self) -> List[Dict[str, Any]]:
        """
        Fetch articles and then extract full article content for each using readability.

        Returns:
            List[Dict[str, Any]]: List of articles with full text added (under key 'full_text')

        Raises:
            NewsApiError: If the API request fails or returns an error
        """
        try:
            logger.info("Extracting full content for articles")
            articles_data = self.get_articles()
            articles = articles_data.get("articles", [])

            logger.info(f"Processing {len(articles)} articles for full content extraction")
            full_articles = []

            for i, article in enumerate(articles):
                article_url = article.get("url")
                if not article_url:
                    logger.warning(f"Article {i + 1} missing URL, skipping")
                    continue

                try:
                    logger.debug(f"Fetching content from URL: {article_url}")
                    response = requests.get(article_url, timeout=10)
                    response.raise_for_status()

                    logger.debug(f"Extracting text with readability from article {i + 1}")
                    content_html = Document(response.text).summary()
                    content_text = html.fromstring(content_html).text_content()

                    article['full_text'] = content_text.strip()
                    logger.debug(f"Successfully extracted {len(content_text)} characters from article {i + 1}")
                    full_articles.append(article)

                except requests.exceptions.RequestException as e:
                    logger.warning(f"Failed to fetch article {i + 1} ({article_url}): {e}")
                    article['full_text'] = f"[Error fetching content: Network error]"
                    full_articles.append(article)
                except Exception as e:
                    logger.warning(f"Failed to extract content for article {i + 1} ({article_url}): {e}")
                    article['full_text'] = f"[Error extracting content: {type(e).__name__}]"
                    full_articles.append(article)

            logger.info(f"Successfully processed {len(full_articles)} articles")
            return full_articles

        except NewsApiError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in extract_full_articles: {e}", exc_info=True)
            raise NewsApiError(f"Failed to extract full articles: {str(e)}") from e