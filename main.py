from datetime import datetime, timedelta

from src.news_data import NewsApiClient

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
