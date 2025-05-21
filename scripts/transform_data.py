import json
import os

def transform_weather():
    base_path = "/opt/airflow/data" if os.getenv("AIRFLOW_HOME") else "data"
    raw_path = os.path.join(base_path, "raw", "weather.json")
    processed_path = os.path.join(base_path, "processed")
    os.makedirs(processed_path, exist_ok=True)

    with open(raw_path, "r") as f:
        data = json.load(f)

    transformed = {
        "city": data["name"], 
        "temperature_celsius": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

    with open(os.path.join(processed_path, "weather_transformed.json"), "w") as f:
        json.dump(transformed, f)

    print(f"✅ Transformed data saved to {processed_path}/weather_transformed.json")

if __name__ == "__main__":
    transform_weather()
