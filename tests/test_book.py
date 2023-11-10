import pytest
import json

from server import app


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

with open('tests/test_book_clubs.json') as c:
        mock_clubs = json.load(c)['clubs']

with open('tests/test_book_competitions.json') as comps:
        mock_competitions = json.load(comps)['competitions']

# Test with a club with 0 point -> try to purchase -1, 0 and 1 place
# Test with a club with 1 point -> try to purchase 0, 1 and 2 places
def test_redeem_more_point(client, monkeypatch):
    monkeypatch.setattr("server.clubs", mock_clubs)
    monkeypatch.setattr("server.competitions", mock_competitions)
    competition = mock_competitions[0]
    
    numberOfPlacesStart = competition['numberOfPlaces']
    for club in mock_clubs:
        for i in [-1, 0, 1]:
            nb_places = int(club['points']) + i
            response = client.post('/purchasePlaces', data={
                'competition': competition['name'],
                'club': club['name'],
                'places': nb_places
            })

            if nb_places < 0:
                assert response.status_code == 400
            elif i == 1:
                assert response.status_code == 403
            else:
                assert response.status_code == 200
                assert int(competition['numberOfPlaces']) == int(numberOfPlacesStart) - nb_places

            
