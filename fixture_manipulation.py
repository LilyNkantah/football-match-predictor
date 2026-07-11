import json
''' 
    This script processes the fixtures data for the 2022/23 Premier League season, 
    and completes all further calculations of stats required for other analysis, such as team matchups for h2h comparisons, team goal stats, and recent form.
'''


'''
    This function extracts unique team ID pairs from the fixtures and saves them to a text file for further analysis or processing. 
    It reads the JSON data from a file, iterates through each fixture, and collects the team IDs in a set to ensure uniqueness. 
    Finally, it saves the unique pairs to a text file.
'''
def extract_unique_team_pairs():
    # 2022/23 SEASON FIXTURES
    with open('fixtures/fixtures_league=39_season=2023.json') as json_file:
        fixtures_file_2023 = json.load(json_file) # Load the JSON data from the file into a Python dictionary

    fixture_team_ids = set()  # Set to store unique team ID pairs for all fixtures

    for fixture in fixtures_file_2023.get('response', []):
        # fixture_id = fixture.get('fixture', {}).get('id')
        # home_team = fixture.get('teams', {}).get('home', {}).get('name')
        home_team_id = fixture.get('teams', {}).get('home', {}).get('id')
        # away_team = fixture.get('teams', {}).get('away', {}).get('name')
        away_team_id = fixture.get('teams', {}).get('away', {}).get('id')
        # date = fixture.get('fixture', {}).get('date')
        # status = fixture.get('fixture', {}).get('status', {}).get('short')
        # if fixture.get('teams', {}).get('home', {}).get('winner') == True:
        #     winner = home_team
        # elif fixture.get('teams', {}).get('away', {}).get('winner') == True:
        #     winner = away_team
        # else:
        #     winner = None # Match ended in a draw

        # Store the team IDs in the set
        fixture_team_ids.add(tuple(sorted([home_team_id, away_team_id])))  # sort to ensure uniqueness regardless of home/away order

    print(f"Total unique team ID pairs for all fixtures: {len(fixture_team_ids)}")
    save_fixtures(fixture_team_ids)  # Save the unique team ID pairs to a text file
    print(f"Unique team ID pairs for all fixtures have been saved to 'remaining_fixtures_for_h2h.txt'.")

def remove_used_fixture(team1_id, team2_id):
    # Read the existing fixtures from the file
    with open("remaining_fixtures_for_h2h.txt", "r") as f:
        fixtures = f.readlines()

    # Create a tuple of the team IDs to remove
    fixture_to_remove = tuple(sorted([team1_id, team2_id]))

    # Filter out the fixture to remove
    updated_fixtures = [fixture for fixture in fixtures if tuple(map(int, fixture.strip()[1:-1].split(','))) != fixture_to_remove]

    print(f"Length before removal: {len(fixtures)}. Removed fixture: {fixture_to_remove}. Remaining fixtures: {len(updated_fixtures)}")

    # Write the updated fixtures back to the file
    save_fixtures([tuple(map(int, fixture.strip()[1:-1].split(','))) for fixture in updated_fixtures])

def save_fixtures(team_ids):
    with open("remaining_fixtures_for_h2h.txt", "w") as f:
        for fixture in team_ids:
            f.write(str(fixture) + "\n")


if __name__ == "__main__":
    extract_unique_team_pairs()
    # extract_seasonal_team_goal_stats()
    # extract_recent_team_form_stats()
