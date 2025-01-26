import requests
import pandas as pd
from datetime import datetime, timedelta

# Replace with your News API key
NEWS_API_KEY = '488360398e404794a2c13d07ec16804f'

# Function to fetch coffee-related news from News API
def fetch_coffee_news():
    news_api_url = "https://newsapi.org/v2/everything"
    query = (
        "(coffee OR \"coffee production\" OR \"coffee export\" OR \"coffee crop\" OR "
        "\"coffee prices\" OR \"coffee industry\" OR \"coffee climate change\" OR "
        "\"coffee supply chain\" OR \"coffee market\" OR \"coffee trade\") AND "
        "(Brazil OR Vietnam OR Colombia OR Ethiopia OR Indonesia OR India OR Honduras OR Uganda OR Peru)"
    )
    query_params = {
        "q": query,
        "from": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        "sortBy": "relevance",
        "language": "en",
        "pageSize": 100,
        "apiKey": NEWS_API_KEY,
    }

    try:
        response = requests.get(news_api_url, params=query_params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        if not articles:
            print("No coffee-related news found.")
            return None

        news_list = [
            {
                "Source": article.get("source", {}).get("name", "Unknown"),
                "Title": article.get("title", "No Title"),
                "Description": article.get("description", "No Description"),
                "Content": article.get("content", "No Content"),
                "Published At": article.get("publishedAt", "Unknown"),
                "URL": article.get("url", "No URL"),
            }
            for article in articles
        ]
        news_df = pd.DataFrame(news_list)
        return news_df
    except Exception as e:
        print(f"Error fetching coffee-related news: {e}")
        return None

# Example usage of the function
if __name__ == "__main__":
    print("Fetching coffee-related news...")
    news_df = fetch_coffee_news()
    if news_df is not None and not news_df.empty:
        news_df.to_csv("coffee_related_news_data.csv", index=False)
        print("Coffee-related news data saved to coffee_related_news_data.csv.")
    else:
        print("No data fetched.")
