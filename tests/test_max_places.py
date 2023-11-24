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
    clubs = mock_clubs
    competition = mock_competitions[0]
    nb_places = [11, 12, 13]
    
    for i in range(3):
        club = clubs[i]
        nb = nb_places[i]

        response = client.post('/purchasePlaces', data={
            'competition': competition['name'],
            'club': club['name'],
            'places': nb
        })

        if nb <= 12:
            assert response.status_code == 200
        else:
            assert response.status_code == 403

            
