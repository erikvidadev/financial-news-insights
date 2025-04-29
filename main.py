from src.news_data import NewsApiClient


news_client = NewsApiClient(source_domain="techcrunch.com",
                            search_query="Nvidia",
                            categories=['Tech', 'Technologies'],
                            start_date="2025-04-11",
                            end_date="2025-04-25",
                            )

news_client.save_response_json()


#response = news_client.fetch_articles()

#print(f"Fetching news from {news_client.start_date} to {news_client.end_date}")
#print(f"Status code: {response.status_code}")

#if response.status_code == 200:
#    print(json.dumps(response.json(), indent=2))
#else:
#    print(f"Error: {response.text}")


