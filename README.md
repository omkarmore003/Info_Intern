# AI-Driven Supply Chain Disruption Predictor and Inventory Optimization System

## Overview
This project is an AI-driven system designed to monitor, predict, and mitigate risks in the coffee bean supply chain. By combining sentiment analysis, risk assessment, and inventory optimization, it provides real-time insights and automates stock adjustments to ensure smooth supply chain operations.

The project consists of four milestones:
1. **Global Data Collection**
2. **Global Data Monitoring and Analysis Engine**
3. **Predictive Disruption Modeling and ERP Integration**
4. **Real-Time Alert and Reporting Dashboard Deployment**

---

## Features
### Milestone 1: Global Data Collection
- **News Data Collection**: Fetches articles about coffee production, trade, prices, and climate-related issues from the News API.
- **Weather Data Collection**: Collects weather information for major coffee-producing regions using the OpenWeatherMap API.
- **Data Storage**: Saves the collected news and weather data in CSV files for further analysis.

### Milestone 2: Global Data Monitoring and Analysis Engine
- **Coffee News Monitoring**: Fetches coffee-related news from global sources using the News API.
- **Sentiment Analysis**: Analyzes the sentiment of news articles using the Meta LLaMA pipeline.
- **Risk Analysis**: Assesses potential supply chain risks using OpenAI's GPT API.
- **Data Aggregation**: Saves sentiment and risk analysis results in CSV files for further processing.

### Milestone 3: Predictive Disruption Modeling and ERP Integration
- **MySQL Database Integration**: Stores inventory and risk data for analysis and adjustments.
- **Stock Adjustment Rules**: Adjusts inventory levels based on risk severity (High, Medium, Low).
- **Automated Inventory Management**: Tracks and updates stock levels in the database.

### Milestone 4: Real-Time Alert and Reporting Dashboard Deployment
- **Interactive Dashboard**: Visualizes risk levels and inventory adjustments using Flask and Matplotlib.
- **HTML Dashboard Template**: Provides a web-based interface for viewing visualizations and insights.
- **Email Notifications**: Sends alerts for critical risks and stock adjustments.
- **Real-Time Insights**: Provides actionable insights through a web-based interface.

---

## Installation
### Prerequisites
- Python 3.8+
- MySQL Database
- News API Key
- OpenWeatherMap API Key
- OpenAI API Key
- Flask

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up the MySQL database:
   - Update database credentials in `inventory.py` and `main.py`.
   - Run the `inventory.py` script to create tables and insert mock data:
     ```bash
     python inventory.py
     ```
4. Obtain API keys:
   - Get a News API key from [NewsAPI](https://newsapi.org/).
   - Get an OpenWeatherMap API key from [OpenWeatherMap](https://openweathermap.org/).
   - Get an OpenAI API key from [OpenAI](https://openai.com/).
   - Update the API keys in `ss.py` and the milestone 1 script.
5. Run the Flask app:
   ```bash
   python main.py
   ```
6. Access the dashboard at [http://127.0.0.1:5000/dashboard](http://127.0.0.1:5000/dashboard).

---

## Usage
### Milestone 1: Data Collection
1. Run the milestone 1 script to fetch news and weather data:
   ```bash
   python news.py
   and python weather.py

   ```
2. The script generates two CSV files:
   - `coffee_supply_chain_news.csv`: Contains news data.
   - `coffee_producing_regions_weather.csv`: Contains weather data for coffee-producing regions.

### Milestone 2: Data Monitoring and Analysis
1. Run the `ss.py` script to analyze sentiment and risks:
   ```bash
   python ss.py
   ```
2. The script generates three CSV files:
   - `coffee_related_news_data.csv`: Raw news data.
   - `sentiment_and_risk_analysis_results.csv`: Combined sentiment and risk analysis.
   - `risky_articles.csv`: Articles flagged for potential risks.

### Milestone 3: Predictive Disruption Modeling
1. Ensure the `sentiment_and_risk_analysis_results.csv` file is present.
2. Run the `inventory.py` script to adjust stock levels based on risks:
   ```bash
   python inventory.py
   ```
3. Check the `adjusted_inventory` table in the database for updated stock levels.

### Milestone 4: Real-Time Dashboard
1. Launch the Flask app using `main.py`:
   ```bash
   python main.py
   ```
2. Visualize:
   - Risk Levels Distribution
   - Inventory Adjustments
3. Review email notifications for critical risks and stock adjustments.
4. Use the HTML template (`dashboard.html`) for a styled and user-friendly interface.

---

## Files
1. **milestone1**: Fetches news and weather data for coffee-producing regions.
2. **milestone2**: Fetches news, performs sentiment and risk analysis, and saves results.
3. **milestone3**: Handles inventory management and adjusts stock levels based on risks.
4. **milestone4**: Hosts the Flask-based dashboard and sends email alerts. Provides a styled web-based interface for visualizing risk and inventory adjustments.

---

## Technologies Used
- **APIs**: NewsAPI, OpenWeatherMap, OpenAI GPT-4
- **Database**: MySQL
- **Data Analysis**: Pandas, Matplotlib
- **Web Framework**: Flask
- **Machine Learning Models**: Meta LLaMA, Transformers

---

## Acknowledgments
- [NewsAPI](https://newsapi.org/)
- [OpenWeatherMap](https://openweathermap.org/)
- [OpenAI](https://openai.com/)
- [Flask](https://flask.palletsprojects.com/)

