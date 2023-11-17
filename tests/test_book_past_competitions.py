import pytest
import json
from datetime import datetime, timedelta


from server import app


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

with open('tests/test_book_past_competitions_clubs.json') as c:
        mock_clubs = json.load(c)['clubs']

with open('tests/test_book_past_competitions.json') as comps:
        mock_competitions = json.load(comps)['competitions']

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
formatted_dates = [day.strftime("%Y-%m-%d %H:%M:%S") for day in [today, yesterday, tomorrow]]

def test_book_past_competitions(client, monkeypatch):
    monkeypatch.setattr("server.clubs", mock_clubs)
    monkeypatch.setattr("server.competitions", mock_competitions)
    club = mock_clubs[0]
    competition = mock_competitions[0]

    for date in formatted_dates:
        competition['date'] = date
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')
        if datetime.strptime(date, "%Y-%m-%d %H:%M:%S") >= today:
            assert response.status_code == 200
        else:
            assert response.status_code == 400
