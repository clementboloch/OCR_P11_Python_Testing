from datetime import datetime, timedelta
import json


def generate_mock_competitions():
    places = ["0", "10", "12", "20"]

    today = datetime.now()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    dates = [day.strftime("%Y-%m-%d %H:%M:%S") for day in [today, yesterday, tomorrow]]

    competitions = []
    i = 0
    for place in places:
        for date in dates:
            i += 1
            competition = {
                "name": f"Competition {i}",
                "date": date,
                "numberOfPlaces": place
            }
            competitions.append(competition)

    competitions_json = {
        "competitions": competitions
    }

    with open('tests/test_global_competitions.json', 'w') as json_file:
        json.dump(competitions_json, json_file, indent=4)
