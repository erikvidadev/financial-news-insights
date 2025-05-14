import nltk
nltk.download("vader_lexicon")

import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Tisztított hírek beolvasása
news_df = pd.read_csv("../data/clean/news/clean_news_data.csv")

# VADER inicializálása
sid = SentimentIntensityAnalyzer()

# Minden hírszövegre kiszámítjuk a compound értéket
news_df["sentiment"] = news_df["full_text"].apply(lambda x: sid.polarity_scores(str(x))["compound"])

# Dátum biztosítása
news_df["date"] = pd.to_datetime(news_df["publishedAt"]).dt.date

# Napi szinten átlagoljuk a hangulatot
daily_sentiment = news_df.groupby("date")["sentiment"].mean().reset_index()

# Kimeneti fájl mentése
daily_sentiment.to_csv("../data/clean/news/sentiment_news_data.csv", index=False)
