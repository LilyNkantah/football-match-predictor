import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

load_dotenv()  # Load environment variables from .env file

def fetch_data():
    # Define API endpoint and secure credentials via env variables
    API_URL = "https://v3.football.api-sports.io/"
    API_KEY = os.getenv("API_FOOTBALL")

    # Set up headers for the API request
    headers = {
        'x-apisports-key': f"{API_KEY}",
        'Content-Type': "application/json"
    }

    print("Fetching data from API...")

    # PREMIER LEAGUE = ID 39
    # SEASONS 2022/23 - 2024/25
    endpoints = [
        # "fixtures/headtohead?league=39&season=2022&h2h=33-34&last=5", will run h2h alone until fulfilled for all teams, then remove
        "fixtures?league=39&season=2024", # run 5 times with correct parameters, then remove
    ]

    for endpoint in endpoints:
        # Make the GET request to the API and receive the JSON response
        data = make_get_request(API_URL + endpoint, headers)

        # Save the data to my SQLite database or to a file for further processing before inserting into the database
        with open(f'{endpoint.replace("?", "_").replace("&", "_")}.json', 'w') as f:
            json.dump(data, f)

        print(f"Data from endpoint '{endpoint}' successfully ingested.")

    
def make_get_request(url, headers):
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        raise e
    
if __name__ == "__main__":
    fetch_data()