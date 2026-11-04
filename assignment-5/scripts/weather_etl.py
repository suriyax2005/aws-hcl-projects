import requests
import csv
from pathlib import Path

def fetch_weather_data():
    """
    Fetch daily maximum temperature data
    from the Open-Meteo weather API.
    """

    cities = {
        "Chennai": {"latitude": 13.0827, "longitude": 80.2707},
        "Mumbai": {"latitude": 19.0760, "longitude": 72.8777},
        "Delhi": {"latitude": 28.6139, "longitude": 77.2090},
        "London": {"latitude": 51.5072, "longitude": -0.1276},
        "New York": {"latitude": 40.7128, "longitude": -74.0060}
    }

    weather_data = []

    for city, coordinates in cities.items():

        url = "https://api.open-meteo.com/v1/forecast"

        params = {
            "latitude": coordinates["latitude"],
            "longitude": coordinates["longitude"],
            "daily": "temperature_2m_max",
            "temperature_unit": "fahrenheit",
            "forecast_days": 1,
            "timezone": "auto"
        }

        response = requests.get(url, params=params, timeout=30)

        response.raise_for_status()

        data = response.json()

        weather_data.append({
            "city": city,
            "date": data["daily"]["time"][0],
            "temperature_f": data["daily"]["temperature_2m_max"][0]
        })

    return weather_data



def save_to_csv(processed_data):
    """
    Save transformed weather records
    into a structured CSV file.
    """

    output_folder = Path(__file__).resolve().parent.parent / "output"

    # Create output folder if it doesn't exist
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "processed_weather.csv"

    fieldnames = [
        "city",
        "date",
        "temperature_f",
        "temperature_c"
    ]

    with open(output_file, mode="w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(processed_data)

    print(f"\nCSV file successfully created: {output_file}")
    print(f"Total cities processed: {len(processed_data)}")


def transform_weather_data(raw_data):
    """
    Convert Fahrenheit to Celsius and keep
    only cities with temperatures above 0°C.
    """

    processed_data = []

    for record in raw_data:

        fahrenheit = record["temperature_f"]

        # Fahrenheit to Celsius conversion
        celsius = (fahrenheit - 32) * 5 / 9

        # Filter cities above freezing
        if celsius > 0:

            processed_record = {
                "city": record["city"],
                "date": record["date"],
                "temperature_f": fahrenheit,
                "temperature_c": round(celsius, 2)
            }

            processed_data.append(processed_record)

    return processed_data



def main():

    print("========== WEATHER ETL PIPELINE ==========")

    # EXTRACT
    print("\n1. Extracting weather data...")

    raw_data = fetch_weather_data()

    print(f"Successfully fetched {len(raw_data)} cities.")

    # TRANSFORM
    print("\n2. Transforming weather data...")

    processed_data = transform_weather_data(raw_data)

    print(f"Cities above freezing: {len(processed_data)}")

    # LOAD
    print("\n3. Saving processed data...")

    save_to_csv(processed_data)

    print("\n========== ETL COMPLETED SUCCESSFULLY ==========")


if __name__ == "__main__":
    main()

