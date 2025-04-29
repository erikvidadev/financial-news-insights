import yfinance as yf


class StockData:
    def __init__(self):
        self.stock_symbols = ["AAPL", "GOOGL", "AMZN", "NVDA"]

    def fetch_stock_data(self):
        stock_data = {}
        for symbol in self.stock_symbols:
            stock_data[symbol] = yf.download(symbol, period="7d", interval="1h")
        return stock_data

