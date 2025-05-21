import json
import os
import psycopg2

def load_to_postgres():
    base_path = "/opt/airflow/data" if os.getenv("AIRFLOW_HOME") else "data"
    transformed_path = os.path.join(base_path, "processed", "weather_transformed.json")
    
    with open(transformed_path, "r") as f:
        data = json.load(f)

    conn = psycopg2.connect(
        host=os.getenv("PG_HOST", "localhost"),
        port=os.getenv("PG_PORT", "5432"),
        dbname=os.getenv("PG_DB", "weatherdb"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD", "postgres")
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city TEXT,
            temperature_celsius FLOAT,
            humidity INT,
            weather TEXT,
            wind_speed FLOAT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        INSERT INTO weather (city, temperature_celsius, humidity, weather, wind_speed)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        data["city"],
        data["temperature_celsius"],
        data["humidity"],
        data["weather"],
        data["wind_speed"]
    ))

    conn.commit()
    cur.close()
    conn.close()

    print("✅ Data loaded into PostgreSQL database.")

if __name__ == "__main__":
    load_to_postgres()
