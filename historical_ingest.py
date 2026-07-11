import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import time

import fixture_manipulation  # Import the fixture_manipulation module to access its functions

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

    # 69 LEFT
    count = 4
    while count > 0:
        # get team IDs for first fixture in the fixtures file
        with open('remaining_fixtures_for_h2h.txt') as f:
            first_line = f.readline().strip('\n')
            first_line = first_line[1:-1]  # Remove the parentheses from the string representation of the tuple
            first_line = first_line.split(',')

            team1_id, team2_id = map(int, first_line)  # Convert the split strings to integers

        endpoint = f"fixtures/headtohead?h2h=" + str(team1_id) + "-" + str(team2_id) # will run h2h alone until fulfilled for all teams, then remove
        
        # Make the GET request to the API and receive the JSON response
        data = make_get_request(API_URL + endpoint, headers)

        # Save the data to my SQLite database or to a file for further processing before inserting into the database
        with open(f'{endpoint.replace("?", "_").replace("&", "_").replace("/", "_")}.json', 'w') as f:
            json.dump(data, f)

        print(f"Data from endpoint '{endpoint}' successfully ingested.")
        
        fixture_manipulation.remove_used_fixture(team1_id, team2_id)  # Remove the used fixture from the text file
        count -= 1  # Decrement the count to eventually exit the loop
        time.sleep(5)  # Sleep for 5 seconds to avoid hitting the API rate limit

    
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