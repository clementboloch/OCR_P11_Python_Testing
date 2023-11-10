import pytest
import json

from server import app


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

with open('tests/test_max_places_clubs.json') as c:
        mock_clubs = json.load(c)['clubs']

with open('tests/test_max_places_competitions.json') as comps:
        mock_competitions = json.load(comps)['competitions']

def test_redeem_more_point(client, monkeypatch):
    monkeypatch.setattr("server.clubs", mock_clubs)
    monkeypatch.setattr("server.competitions", mock_competitions)
    club = mock_clubs[0]
    competition = mock_competitions[0]
    
    for club in mock_clubs:
        for nb_places in [11, 12, 13]:
            response = client.post('/purchasePlaces', data={
                'competition': competition['name'],
                'club': club['name'],
                'places': nb_places
            })

            if nb_places <= 12:
                assert response.status_code == 200
            else:
                assert response.status_code == 403

            
