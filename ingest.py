import os
import requests
import json
from datetime import datetime

def fetch_data():
    # Define API endpoint and secure credentials via env variables
    API_URL = ""
    API_KEY = os.getenv("API_FOOTBALL_KEY")

    # Set up headers for the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print("Fetching data from API at ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " UTC...")

    try:
        # Make the GET request to the API
        response = requests.get(API_URL, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response.json()

        # Save the data to my SQLite database or to a file for further processing before inserting into the database

        print("Data successfully ingested.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        raise e
    
if __name__ == "__main__":
    fetch_data()