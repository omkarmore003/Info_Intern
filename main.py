import requests
import pandas as pd

# Constants
API_KEY = '4cbb657dc0694e769d1ee8aae7dfd427'  
BASE_URL = 'https://newsapi.org/v2/everything'

def fetch_news(query, from_date, page=1):
    """Fetch news articles from NewsAPI."""
    params = {
        'q': query,            # Search keyword
        'from': from_date,     # Start date for articles
        'sortBy': 'publishedAt',  # Sort articles by publication date
        'apiKey': API_KEY,     # Your API key
        'page': page,          # Pagination (default 1)
        'pageSize': 20         # Number of articles per page
    }
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

def process_data(data):
    """Extract relevant fields from the API response."""
    articles = data.get('articles', [])
    processed = []
    for article in articles:
        processed.append({
            'title': article['title'],
            'description': article['description'],
            'content': article['content'],
            'publishedAt': article['publishedAt'],
            'source': article['source']['name'],
            'url': article['url']
        })
    return processed

def main():
    query = "supply chain disruption"
    from_date = "2024-12-11"
    data = fetch_news(query, from_date)
    
    if data:
        processed_data = process_data(data)
        # Convert to DataFrame for easy handling
        df = pd.DataFrame(processed_data)
        print(df.head())  # Preview the data
        # Save to CSV
        df.to_csv('news_data.csv', index=False)
        print("Data saved to news_data.csv")

if __name__ == "__main__":
    main()


