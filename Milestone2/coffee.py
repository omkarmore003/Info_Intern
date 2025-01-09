import time
import openai
import pandas as pd
import requests
from transformers import pipeline
from datetime import datetime, timedelta

# Set OpenAI API key
openai.api_key = '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'  # Replace with your OpenAI API key

# OpenWeatherMap API key
OWM_API_KEY = '0acf22103205e7955eb381a520fa9842'  # Replace with your OpenWeatherMap API key

# Replace with your News API key
NEWS_API_KEY = '488360398e404794a2c13d07ec16804f'  # Replace with your News API key

# Initialize Meta LLaMA pipeline for sentiment analysis (using a BART model for text classification)
llama_sentiment_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")

# Function to fetch weather data for coffee-producing countries
def fetch_weather_data(city_name):
    weather_api_url = f"http://api.openweathermap.org/data/2.5/weather"
    query_params = {
        "q": city_name,
        "appid": OWM_API_KEY,
        "units": "metric",
        "lang": "en"
    }
    
    try:
        response = requests.get(weather_api_url, params=query_params)
        response.raise_for_status()
        data = response.json()
        weather_data = {
            "City": city_name,
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Wind Speed": data["wind"]["speed"],
            "Humidity": data["main"]["humidity"],
            "Weather ID": data["weather"][0]["id"]
        }
        return weather_data
    except Exception as e:
        print(f"Error fetching weather data for {city_name}: {e}")
        return None

# Function to fetch coffee-related news from News API
def fetch_coffee_news():
    news_api_url = "https://newsapi.org/v2/everything"
    query = (
        "(coffee OR \"coffee production\" OR \"coffee export\" OR \"coffee crop\" OR "
        "\"coffee prices\" OR \"coffee industry\" OR \"coffee climate change\" OR "
        "\"coffee supply chain\" OR \"coffee market\") AND "
        "(Brazil OR Vietnam OR Colombia OR Ethiopia OR Indonesia OR India OR Honduras OR Uganda OR Peru)"
    )
    query_params = {
        "q": query,
        "from": (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'),
        "sortBy": "relevance",
        "language": "en",
        "pageSize": 30,
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

# Function to analyze sentiment using Meta's LLaMA (BART model for text classification)
def analyze_sentiment(text):
    try:
        sentiment_analysis = llama_sentiment_pipeline(text)
        sentiment = sentiment_analysis[0]['label']
        return sentiment
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error"

# Function to analyze risk using OpenAI's GPT-4o-mini model
def analyze_risk(text):
    messages = [
        {"role": "system", "content": "You are an assistant that analyzes supply chain risks."},
        {"role": "user", "content": f"Does the following text mention any supply chain risks? {text}"}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Use gpt-4o-mini model for risk analysis
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        risk_analysis = response['choices'][0]['message']['content'].strip()

        # Define keywords for risk detection
        risk_keywords = ["disruption", "negative", "storm", "flood", "delay", "supply chain issues", "weather event", "extreme", "damage"]
        risk_detected = any(keyword in risk_analysis.lower() for keyword in risk_keywords)

        time.sleep(20)  # Wait 20 seconds before making the next API call
        return risk_analysis, risk_detected
    except openai.error.OpenAIError as e:
        print(f"Error during risk analysis: {e}")
        return "Error", False

# Retry logic for sentiment and risk analysis functions
def analyze_sentiment_and_risk_with_retry(text, retries=3, delay=20):
    """
    Analyze sentiment and risk with retry logic in case of rate limit errors.

    Parameters:
    - text: News article content or description.
    - retries: The number of retry attempts.
    - delay: Delay in seconds between retries.

    Returns:
    - sentiment: The sentiment of the text.
    - risk_analysis: The risk analysis result.
    - risk_detected: Whether supply chain risks are mentioned.
    """
    for attempt in range(retries):
        try:
            sentiment = analyze_sentiment(text)  # Call the analyze_sentiment function
            risk_analysis, risk_detected = analyze_risk(text)  # Call the analyze_risk function
            return sentiment, risk_analysis, risk_detected
        except Exception as e:
            if attempt < retries - 1:
                print(f"Error: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)  # Wait before retrying
            else:
                print("Max retries reached. Skipping this request.")
                return "Error", "Error", False

# Function to process the fetched news data and perform sentiment and risk analysis
def process_and_analyze_sentiment_and_risk(news_df):
    results = []
    for _, row in news_df.iterrows():
        content = row['Content']  # Assuming 'Content' is the column with news text
        title = row['Title']  # Assuming 'Title' is the column with the article title
        print(f"Analyzing: {title}")

        # Perform sentiment and risk analysis with retry logic
        sentiment, risk_analysis, risk_detected = analyze_sentiment_and_risk_with_retry(content)

        # Save results
        results.append({
            "Title": title,
            "Source": row['Source'],
            "Published At": row['Published At'],
            "Sentiment": sentiment,
            "Risk Analysis": risk_analysis,
            "Risk Detected": risk_detected
        })

    # Return results as DataFrame
    sentiment_and_risk_results_df = pd.DataFrame(results)
    return sentiment_and_risk_results_df

# Main function
def main():
    print("Fetching coffee-related news...")
    news_df = fetch_coffee_news()
    if news_df is None or news_df.empty:
        print("No data fetched.")
        return

    # Fetch weather data for each coffee-producing country (you can customize this list)
    countries = ["Brazil", "Vietnam", "Colombia", "Ethiopia", "Indonesia", "India", "Honduras", "Uganda", "Peru"]
    weather_data_list = []
    for country in countries:
        weather_data = fetch_weather_data(country)
        if weather_data:
            weather_data_list.append(weather_data)

    # Convert weather data to DataFrame
    weather_df = pd.DataFrame(weather_data_list)

    print("Processing and analyzing sentiment and risk...")
    sentiment_and_risk_results_df = process_and_analyze_sentiment_and_risk(news_df)

    # Save the sentiment and risk analysis results to a new CSV file
    sentiment_and_risk_results_df.to_csv("sentiment_and_risk_analysis_results.csv", index=False)
    print("Sentiment and risk analysis results saved to sentiment_and_risk_analysis_results.csv.")

    # Save weather data to CSV
    weather_df.to_csv("weather_data.csv", index=False)
    print("Weather data saved to weather_data.csv.")

    # Optional: Filter and print risky articles
    risky_articles = sentiment_and_risk_results_df[sentiment_and_risk_results_df['Risk Detected'] == True]
    print(f"\nFound {len(risky_articles)} articles with potential risks.")
    print(risky_articles[['Title', 'Sentiment', 'Risk Analysis', 'Risk Detected']])

if __name__ == "__main__":
    main()
