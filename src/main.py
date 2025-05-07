from news_api import NewsApiClient
from src.news_data_handler import NewsDataHandler
from src.stock_data_handler import StockDataHandler
from src.yahoo_finance import YahooFinanceClient


articles_from_newsAPI = NewsApiClient(
    search_query="apple",
    categories="tech",
    search_days=30,
)

news_data_handler = NewsDataHandler()


articles = articles_from_newsAPI.get_articles()
raw_articles = news_data_handler.save_raw_data(articles)
processed_articles = news_data_handler.process_raw_data(raw_articles)
news_data_handler.export_articles(processed_articles)



stock_data_from_yahoo = YahooFinanceClient(
    stock_symbol="AAPL",
    period="1d",
    interval="1h"
)

stock_data_handler = StockDataHandler()

stocks = stock_data_from_yahoo.fetch_stock_data()
stock_data_handler.export_to_all_formats(stocks)

