import time
import openai
import pandas as pd
import requests
from transformers import pipeline
from datetime import datetime, timedelta

# Set OpenAI API key
openai.api_key = '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'

# Replace with your News API key
NEWS_API_KEY = '488360398e404794a2c13d07ec16804f'

# Initialize Meta LLaMA pipeline for sentiment analysis
llama_sentiment_pipeline = pipeline("text-classification", model="facebook/bart-large-mnli")

# Expanded list of risk-related keywords for detecting disruptions
expanded_risk_keywords = [
    "disruption", "negative", "storm", "flood", "delay", 
    "supply chain issues", "weather event", "extreme", "damage", 
    "crop failure", "harvest", "trade conflict", "transportation issues", 
    "drought", "political instability", "tariffs", "blockage", "import/export delays",
    "coffee prices increase", "rising coffee prices", "price surge", "coffee price spike",
    "climate change", "extreme temperatures", "deforestation", "soil degradation", 
    "pest outbreaks", "coffee rust", "water scarcity", "trade embargoes", "currency fluctuations",
    "export bans", "political instability", "labor strikes", "tariffs", "taxes", "import/export restrictions",
    "shipping delays", "port congestion", "freight cost increases", "transportation failure",
    "fuel price volatility", "logistic route disruptions", "price volatility", "raw material fluctuation",
    "inflation", "recession", "consumer behavior change", "competition", "worker shortages",
    "wage strikes", "seasonal unavailability", "cybersecurity threats", "IT failures", "supply chain tracking failures",
    "cargo theft", "social unrest", "human rights violations", "child labor", "Fair Trade compliance"
]


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

# Function to analyze sentiment using Meta's LLaMA
def analyze_sentiment(text):
    try:
        sentiment_analysis = llama_sentiment_pipeline(text, return_all_scores=True)
        scores = {item["label"]: item["score"] for item in sentiment_analysis[0]}
        sentiment = max(scores, key=scores.get)
        sentiment_score = scores[sentiment]
        return sentiment, sentiment_score
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return "Error", 0.0

# Function to analyze risk using OpenAI and detect keywords
def analyze_risk(text):
    messages = [
        {"role": "system", "content": "You are an assistant that analyzes supply chain risks."},
        {"role": "user", "content": f"Assess the following text for supply chain risks and provide a risk score between 0 and 1: {text}"}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        risk_analysis = response['choices'][0]['message']['content'].strip()
        risk_score = 0.0
        for line in risk_analysis.split("\n"):
            if "Risk Score:" in line:
                try:
                    risk_score = float(line.split(":")[1].strip())
                    break
                except ValueError:
                    pass

        risk_detected = any(keyword in risk_analysis.lower() for keyword in expanded_risk_keywords)

        # Fallback: If no score, assign 0.5 for keyword presence
        if risk_score == 0.0 and risk_detected:
            risk_score = 0.5

        return risk_analysis, risk_score, risk_detected
    except openai.error.RateLimitError:
        print("Rate limit reached. Waiting 20 seconds before retrying...")
        time.sleep(20)
        return analyze_risk(text)
    except openai.error.OpenAIError as e:
        print(f"Error during risk analysis: {e}")
        return "Error", 0.0, False

# Function to determine risk level category based on risk score
def categorize_risk_level(risk_score):
    if risk_score >= 0.7:
        return "High"
    elif risk_score >= 0.4:
        return "Medium"
    else:
        return "Low"

# Combine sentiment and risk scores into a decision matrix
def combine_sentiment_and_risk(sentiment_score, risk_score):
    # Example decision matrix for combining sentiment and risk
    if sentiment_score > 0.7 and risk_score > 0.7:
        return "High Risk - Negative Sentiment"
    elif sentiment_score > 0.7 and risk_score <= 0.7:
        return "Moderate Risk - Negative Sentiment"
    elif sentiment_score <= 0.7 and risk_score > 0.7:
        return "High Risk - Neutral/Positive Sentiment"
    else:
        return "Low Risk - Neutral Sentiment"

# Process news data and analyze sentiment and risk
def process_and_analyze_sentiment_and_risk(news_df):
    results = []
    for _, row in news_df.iterrows():
        content = row['Content']
        title = row['Title']
        description = row['Description']
        print(f"Analyzing: {title}")

        sentiment, sentiment_score = analyze_sentiment(content)
        risk_analysis, risk_score, risk_detected = analyze_risk(content)
        risk_level = categorize_risk_level(risk_score)
        combined_analysis = combine_sentiment_and_risk(sentiment_score, risk_score)

        results.append({
            "Title": title,
            "Source": row['Source'],
            "Description": description,
            "Published At": row['Published At'],
            "Sentiment": sentiment,
            "Sentiment Score": sentiment_score,
            "Risk Analysis": risk_analysis,
            "Risk Score": risk_score,
            "Risk Detected": risk_detected,
            "Risk Level": risk_level,
            "Combined Analysis": combined_analysis
        })

    sentiment_and_risk_results_df = pd.DataFrame(results)
    return sentiment_and_risk_results_df

# Main function
def main():
    print("Fetching coffee-related news...")
    news_df = fetch_coffee_news()
    if news_df is None or news_df.empty:
        print("No data fetched.")
        return

    news_df.to_csv("coffee_related_news_data.csv", index=False)
    print("Coffee-related news data saved to coffee_related_news_data.csv.")

    print("Processing and analyzing sentiment and risk...")
    sentiment_and_risk_results_df = process_and_analyze_sentiment_and_risk(news_df)

    sentiment_and_risk_results_df.to_csv("sentiment_and_risk_analysis_results.csv", index=False)
    print("Sentiment and risk analysis results saved to sentiment_and_risk_analysis_results.csv.")

    risky_articles = sentiment_and_risk_results_df[
        (sentiment_and_risk_results_df['Risk Score'] > 0.5) | (sentiment_and_risk_results_df['Risk Detected'])
    ]
    risky_articles.to_csv("risky_articles.csv", index=False)
    print(f"Risky articles saved to risky_articles.csv.\nFound {len(risky_articles)} articles with potential risks.")

    if not risky_articles.empty:
        print(risky_articles[["Title", "Description", "Sentiment", "Sentiment Score", "Risk Analysis", "Risk Score", "Risk Detected", "Risk Level", "Combined Analysis"]])
    else:
        print("No risky articles detected.")

if __name__ == "__main__":
    main()
