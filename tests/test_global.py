import pytest
import json
from datetime import datetime

from server import app
from tests.mock_club_generator import generate_mock_clubs
from tests.mock_competition_generator import generate_mock_competitions

clubs_tested_info = generate_mock_clubs()
generate_mock_competitions()

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

with open('tests/test_global_clubs.json') as c:
        clubs = json.load(c)['clubs']

with open('tests/test_global_competitions.json') as comps:
        competitions = json.load(comps)['competitions']

clubs_name = [club['name'] for club in clubs]

@pytest.mark.parametrize("club_info", clubs_tested_info)
def test_connection(client, monkeypatch, club_info):
    monkeypatch.setattr("server.clubs", clubs)
    response = client.post('/showSummary', data={'email': club_info['email']})
    authorized_clubs_email = [club['email'] for club in clubs]
    if club_info['email'] in authorized_clubs_email:
        assert response.status_code == 200
    else:
        assert response.status_code == 403


@pytest.mark.parametrize("competition_info", competitions)
@pytest.mark.parametrize("club_info", clubs)
def test_book_competitions(client, monkeypatch, competition_info, club_info):
    monkeypatch.setattr("server.clubs", clubs)
    monkeypatch.setattr("server.competitions", competitions)

    response = client.get(f'/book/{competition_info["name"]}/{club_info["name"]}')
    if club_info['name'] not in clubs_name:
        assert response.status_code == 400
    elif datetime.strptime(competition_info["date"], "%Y-%m-%d %H:%M:%S") >= datetime.now():
        assert response.status_code == 200
    else:
        assert response.status_code == 400


@pytest.mark.parametrize("competition_info", competitions)
@pytest.mark.parametrize("club_info", clubs)
def test_book_places(client, monkeypatch, competition_info, club_info):
    monkeypatch.setattr("server.clubs", clubs)
    monkeypatch.setattr("server.competitions", competitions)
    
    initialPlaces = competition_info['numberOfPlaces']
    initialPoints = club_info['points']

    for i in [-1, 0, 1]:
        nb_places = int(club_info['points']) + i
        response = client.post('/purchasePlaces', data={
            'competition': competition_info['name'],
            'club': club_info['name'],
            'places': nb_places
        })

        # Skip past competitions
        if datetime.strptime(competition_info["date"], "%Y-%m-%d %H:%M:%S") < datetime.now():
            continue

        # Test to book negative number of places
        if nb_places < 0:
            assert response.status_code == 400
            continue

        # Test to redeem more points than available
        if i == 1:
            assert response.status_code == 403
            continue

        # Test to redeem more than 12 places
        if nb_places > 12:
            assert response.status_code == 403
            continue
        
        # Test to buy more places than available
        if nb_places > int(competition_info['numberOfPlaces']):
            assert response.status_code == 403
            continue
        
        assert response.status_code == 200
        # Test competition update
        assert int(competition_info['numberOfPlaces']) == int(initialPlaces) - nb_places
        # Test club update
        assert int(club_info['points']) == int(initialPoints) - nb_places
    

