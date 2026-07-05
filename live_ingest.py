import os
import requests
import json
from datetime import datetime

def fetch_data():
    # Define API endpoint and secure credentials via env variables
    API_URL = "https://v3.football.api-sports.io/"
    API_KEY = os.getenv("API_FOOTBALL")

    # Set up headers for the API request
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    print("Fetching data from API at ", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " UTC...")

    try:
        # Make the GET request to the API
        response1 = requests.get(API_URL + "teams/statistics?league=39&team=33&season=2021", headers=headers, timeout=30) # timeout to ensure script never hangs indefinitely
        response2 = requests.get(API_URL + "fixtures?league=39&season=2021", headers=headers, timeout=30)

        response1.raise_for_status()  # Raise an error for bad responses

        # Parse the JSON response
        data = response1.json()

        # Save the data to my SQLite database or to a file for further processing before inserting into the database

        print("Data successfully ingested.")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        raise e
    
if __name__ == "__main__":
    fetch_data()