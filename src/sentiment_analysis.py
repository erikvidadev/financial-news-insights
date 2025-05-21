import logging
from pathlib import Path

import nltk
import pandas as pd
from pandas import DataFrame
from nltk.sentiment.vader import SentimentIntensityAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NLTKResourceManager:
    """Manages downloading and verifying NLTK resources."""

    _vader_lexicon_downloaded = False

    @classmethod
    def ensure_vader_lexicon(cls) -> None:
        """
        Ensure the VADER lexicon resource is downloaded.

        This method downloads the VADER lexicon if not already present
        in the NLTK data directory.
        """
        if cls._vader_lexicon_downloaded:
            return

        try:
            nltk.data.find('sentiment/vader_lexicon.zip')
            cls._vader_lexicon_downloaded = True
        except LookupError:
            logger.info("Downloading VADER lexicon")
            nltk.download("vader_lexicon", quiet=True)
            cls._vader_lexicon_downloaded = True


class NewsSentimentAnalyzer:
    """Performs sentiment analysis on news article text."""

    def __init__(
            self,
            full_output_path: str = "./data/processed/articles_with_sentiment_score.csv",
    ) -> None:
        """
        Initialize the sentiment analyzer.

        Args:
            full_output_path: Path to save the full sentiment analysis results
        """
        NLTKResourceManager.ensure_vader_lexicon()

        self._sentiment_analyzer = SentimentIntensityAnalyzer()
        self._full_output_path = full_output_path

        Path(self._full_output_path).parent.mkdir(parents=True, exist_ok=True)

    def calculate_articles_sentiment(self, news_data: DataFrame) -> DataFrame:
        """
        Calculate sentiment for each article and store it in the dataframe.

        Args:
            news_data: DataFrame containing news articles with at least 'full_text'
                      and 'publishedAt' columns

        Returns:
            DataFrame with added 'sentiment' and 'date' columns

        Raises:
            ValueError: If required columns are missing
        """
        required_columns = ["full_text", "publishedAt"]
        missing_columns = [col for col in required_columns if col not in news_data.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        result_data = news_data.copy()

        logger.info("Calculating sentiment for %d articles", len(result_data))
        result_data["sentiment"] = result_data["full_text"].apply(
            lambda x: self._sentiment_analyzer.polarity_scores(str(x))["compound"]
        )

        result_data["date"] = pd.to_datetime(result_data["publishedAt"]).dt.date
        return result_data

    def export_to_csv(self, news_data: DataFrame) -> None:
        """
        Export both detailed and aggregated sentiment data to CSV files.

        Args:
            news_data: DataFrame with article-level sentiment data

        Raises:
            IOError: If there's an issue writing the files
        """
        try:
            if self._full_output_path:
                logger.info(f"Exporting detailed sentiment data to {self._full_output_path}")
                news_data.to_csv(self._full_output_path, index=False)

        except Exception as e:
            logger.error(f"Error exporting data: {str(e)}")
            raise IOError(f"Failed to export sentiment data: {str(e)}") from e
