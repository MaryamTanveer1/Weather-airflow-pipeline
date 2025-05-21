import requests

import json
import os

def fetch_weather():
    print("📡 Fetching weather data...")  # Add this
    API_KEY = os.getenv("WEATHER_API_KEY")
    city = "Islamabad"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    # Determine save path based on environment
    base_path = "/opt/airflow/data/raw" if os.getenv("AIRFLOW_HOME") else "data/raw"
    os.makedirs(base_path, exist_ok=True)

    file_path = os.path.join(base_path, "weather.json")
    with open(file_path, "w") as f:
        json.dump(data, f)

    print(f"✅ Weather data fetched and saved to {file_path}")

# ✅ Add this so the function actually runs
if __name__ == "__main__":
    fetch_weather()
