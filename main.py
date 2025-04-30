from datetime import datetime, timedelta

from src.news_data import NewsApiClient
from src.stock_data import StockData

end_date = datetime.today()
start_date = end_date - timedelta(days=30)

end_date_str = end_date.strftime('%Y-%m-%d')
start_date_str = start_date.strftime('%Y-%m-%d')


news_client = NewsApiClient(
                            search_query="apple",
                            start_date=start_date_str,
                            end_date=end_date_str,
                            )

news_client.save_response_json()

stock_client = StockData(
    stock_symbol="AAPL",
    period="30d",
    interval="1h"
)
stock_client.save_stock_data_to_files()