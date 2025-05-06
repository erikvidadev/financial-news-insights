from news_api import NewsApiClient
from src.news_data_handler import NewsDataHandler
from src.yahoo_finance import YahooFinanceClient


articles_from_newsAPI = NewsApiClient(
    search_query="apple",
    categories="tech",
    search_days=3,
)

news_data_handler = NewsDataHandler()


articles = articles_from_newsAPI.get_articles()
raw_articles = news_data_handler.save_raw_data(articles)
processed_articles = news_data_handler.process_raw_data(raw_articles)
news_data_handler.export_to_csv(processed_articles)
news_data_handler.export_to_excel(processed_articles)



stock_data_from_yahoo = YahooFinanceClient(
    stock_symbol="AAPL",
    period="30d",
    interval="1h"
)
