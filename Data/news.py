import requests
import pandas as pd
from datetime import datetime
import csv

# Replace with your actual News API key
NEWS_API_KEY = "4cbb657dc0694e769d1ee8aae7dfd427"

# Base URL for the News API
news_api_url = "https://newsapi.org/v2/everything"

# Function to fetch news data from the API
def fetch_news(url, params):
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch news. Status code: {response.status_code}")
        return None

# Function to handle pagination and fetch all news articles
def fetch_and_process_news(url, params):
    all_articles = []  # List to hold all the fetched articles
    page = 1  # Start from page 1
    
    while True:
        params["page"] = page  # Set the current page number
        print(f"Fetching page {page}...")  # Print the page number for tracking
        
        # Fetch news data for the current page
        news_data = fetch_news(url, params)
        
        if news_data and news_data.get('articles'):
            articles = news_data['articles']
            all_articles.extend(articles)  # Add articles to the list
            
            print(f"Page {page} fetched with {len(articles)} articles.")
            
            # If fewer than 20 articles are returned, stop as it's the last page
            if len(articles) < 20:
                print("No more articles found, exiting.")
                break
            else:
                page += 1  # Go to the next page
        else:
            print("Error or no articles returned. Stopping.")
            break

    return all_articles

# Define query parameters
query_params = {
    "q": "coffee supply chain",  # Broad query for coffee supply chain
    "from": (datetime.now() - pd.Timedelta(days=7)).strftime('%Y-%m-%d'),  # Last 7 days
    "sortBy": "relevance",  # Sort articles by relevance
    "apiKey": NEWS_API_KEY,  # Your News API key
    "language": "en",  # Optional: Specify language
    "pageSize": 50  # Set the page size to 20 (default)
}

# Fetch all news articles with pagination
all_articles = fetch_and_process_news(news_api_url, query_params)

# If articles were fetched, save them to a CSV file
if all_articles:
    csv_filename = "coffee_supply_chain_news.csv"
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Description", "URL", "Published At"])  # Header row
        
        # Write each article to the CSV file
        for article in all_articles:
            title = article.get('title', 'No title available')
            description = article.get('description', 'No description available')
            url = article.get('url', 'No URL available')
            published_at = article.get('publishedAt', 'No published date')
            
            writer.writerow([title, description, url, published_at])
    
    print(f"News data saved to {csv_filename}")
else:
    print("No news articles found.")
