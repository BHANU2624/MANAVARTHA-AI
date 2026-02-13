import pandas as pd

class NewsLoader:
    def __init__(self):
        self.df = pd.read_csv("data/all_telugu_news_articles.csv")

    def latest_articles(self, n=20):
        df_sorted = self.df.sort_values(by="date", ascending=False)
        return df_sorted.head(n).to_dict(orient="records")

    def fetch_article(self, url: str):
        row = self.df[self.df["url"] == url]
        if row.empty:
            return None
        return row.iloc[0].to_dict()
