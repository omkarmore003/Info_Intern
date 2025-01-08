import requests
import pandas as pd
from datetime import datetime
import openai
from transformers import pipeline
import time
import json

# Replace with your API keys
OPENAI_API_KEY = "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"  # Replace with your OpenAI API key
NEWS_API_KEY = "488360398e404794a2c13d07ec16804f"      # Replace with your News API key

# Initialize OpenAI GPT
def initialize_openai():
    openai.api_key = OPENAI_API_KEY

# Initialize LLaMA (or an alternative Hugging Face model)
def initialize_llama():
    return pipeline("text-classification", model="facebook/bart-large-mnli")

# Fetch news data from the News API
def fetch_news(api_url, query_params):
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

# Analyze risk using OpenAI GPT with rate limit handling
def analyze_risk_with_gpt(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Replace with a model you have access to
            messages=[
                {"role": "system", "content": "You are an expert in supply chain risk analysis."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message['content']
    except openai.error.RateLimitError:
        print("Rate limit reached. Waiting 20 seconds...")
        time.sleep(20)  # Wait before retrying
        return analyze_risk_with_gpt(content)  # Retry the request
    except Exception as e:
        print(f"Error with OpenAI GPT: {e}")
        return "GPT analysis failed."

# Perform sentiment analysis using LLaMA
def analyze_sentiment_with_llama(content, llama_pipeline):
    try:
        results = llama_pipeline(content)
        return results
    except Exception as e:
        print(f"Error with LLaMA: {e}")
        return "LLaMA sentiment analysis failed."

# Aggregate news data into a structured format
def aggregate_data(news_data):
    try:
        articles = news_data.get('articles', [])
        if not articles:
            print("No articles found in the response.")
            return pd.DataFrame()
        structured_data = []
        for article in articles:
            structured_data.append({
                "source": article.get('source', {}).get('name', 'Unknown'),
                "title": article.get('title', 'No Title'),
                "description": article.get('description', 'No Description'),
                "content": article.get('content', 'No Content'),
                "published_at": article.get('publishedAt', 'Unknown')
            })
        return pd.DataFrame(structured_data)
    except Exception as e:
        print(f"Error structuring data: {e}")
        return None

# Main pipeline
def main():
    # Initialize models
    initialize_openai()
    llama_pipeline = initialize_llama()
    
    # Fetch news data
    news_api_url = "https://newsapi.org/v2/everything"
    query_params = {
        "q": "coffee OR coffee production OR coffee export OR coffee crop OR coffee prices OR climate change coffee",  # Adjust query for broader results
        "from": (datetime.now() - pd.Timedelta(days=7)).strftime('%Y-%m-%d'),  # Last 7 days
        "sortBy": "relevance",
        "apiKey": NEWS_API_KEY,
        "pageSize": 50
    }
    news_data = fetch_news(news_api_url, query_params)
    
    # Log API response
    if not news_data:
        print("Failed to fetch news data.")
        return
    print("News API Response:")
    print(json.dumps(news_data, indent=2))  # Log full response for debugging
    
    # Aggregate data
    structured_data = aggregate_data(news_data)
    if structured_data is None or structured_data.empty:
        print("No structured data available.")
        return
    
    # Analyze risk and sentiment
    results = []
    for _, row in structured_data.iterrows():
        print(f"Analyzing article: {row['title']}")
        
        # Risk Analysis with GPT
        gpt_analysis = analyze_risk_with_gpt(row['content'])
        
        # Sentiment Analysis with LLaMA
        sentiment_analysis = analyze_sentiment_with_llama(row['content'], llama_pipeline)
        
        # Append analysis results
        results.append({
            "Title": row['title'],
            "Source": row['source'],
            "Published At": row['published_at'],
            "Risk Analysis (GPT)": gpt_analysis,
            "Sentiment Analysis (LLaMA)": sentiment_analysis
        })
        time.sleep(1)  # Ensure delays between requests to avoid rate limits
    
    # Convert results to a DataFrame and save to CSV
    results_df = pd.DataFrame(results)
    results_df.to_csv("chain_analysis.csv", index=False)
    print("Analysis complete. Results saved to chain_analysis.csv.")

if __name__ == "__main__":
    main()
