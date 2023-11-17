import pytest
import json
from copy import deepcopy

from server import app


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

with open('tests/test_points_update_clubs.json') as c:
        mock_clubs = json.load(c)['clubs']

with open('tests/test_points_update_comptitions.json') as comps:
        mock_competitions = json.load(comps)['competitions']

def test_redeem_more_point(client, monkeypatch):
    monkeypatch.setattr("server.competitions", mock_competitions)
    competition = mock_competitions[0]

    club = mock_clubs[0]
    initialPoints = int(club['points'])
    for nbPlaces in range(initialPoints + 1):
        clubs = deepcopy(mock_clubs)
        monkeypatch.setattr("server.clubs", clubs)
        club = clubs[0]
        response = client.post('/purchasePlaces', data={
            'competition': competition['name'],
            'club': club['name'],
            'places': nbPlaces
        })
        newPoints = int(club['points'])
        assert newPoints == initialPoints - nbPlaces
