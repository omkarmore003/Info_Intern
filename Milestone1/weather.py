import requests
import csv

# Your OpenWeatherMap API key
API_KEY = "0acf22103205e7955eb381a520fa9842"

# Base URL for the OpenWeatherMap API (Current weather endpoint)
url = "http://api.openweathermap.org/data/2.5/weather"

# List of specific coffee-producing regions or cities (with country names)
coffee_regions = [
    "Manaus, Brazil",        # Major coffee region in Brazil
    "Ho Chi Minh City, Vietnam",  # Major coffee region in Vietnam
    "Medellín, Colombia",    # Major coffee region in Colombia
    "Addis Ababa, Ethiopia",  # Capital of Ethiopia, coffee-producing country
    "Bali, Indonesia",       # Known coffee-growing region in Indonesia
    "Bangalore, India",      # Known coffee-producing city in India
    "Tegucigalpa, Honduras", # Capital of Honduras, coffee-producing country
    "Kampala, Uganda",       # Capital of Uganda, coffee-producing country
    "Guatemala City, Guatemala", # Capital of Guatemala, coffee-producing country
    "Lima, Peru"             # Capital of Peru, coffee-producing country
]

# Function to fetch weather data for a specific region or city
def fetch_weather(region_name, api_key):
    # Set up the parameters for the API request
    params = {
        "q": region_name,           # City/Region name (e.g., "Manaus, Brazil")
        "appid": api_key,           # API Key
        "units": "metric",          # Units for temperature (metric: Celsius, imperial: Fahrenheit)
        "lang": "en"                # Language for the response (optional)
    }
    
    # Send GET request to the OpenWeatherMap API
    response = requests.get(url, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data from the response
        weather_data = response.json()
        return weather_data
    else:
        print(f"Error: Unable to fetch weather data for {region_name}. Status code: {response.status_code}")
        return None

# Define the CSV file name to store the weather data
csv_filename = "coffee_producing_regions_weather.csv"

# Open the CSV file for writing
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    # Define the fieldnames for the CSV file
    fieldnames = ["Region", "Temperature (°C)", "Humidity (%)", "Weather", "Wind Speed (m/s)"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Fetch weather data for each specific coffee-producing region
    for region in coffee_regions:
        print(f"\nFetching weather data for {region}...")
        
        # Fetch weather data for the specified region
        weather_data = fetch_weather(region, API_KEY)
        
        # If data is fetched successfully, write it to the CSV
        if weather_data:
            row = {
                "Region": region,
                "Temperature (°C)": weather_data['main']['temp'],
                "Humidity (%)": weather_data['main']['humidity'],
                "Weather": weather_data['weather'][0]['description'],
                "Wind Speed (m/s)": weather_data['wind']['speed']
            }
            writer.writerow(row)
            print(f"Weather data for {region} written to CSV.")
        else:
            print(f"No weather data found for {region}.")

print(f"Weather data for specific coffee-producing regions saved to {csv_filename}")