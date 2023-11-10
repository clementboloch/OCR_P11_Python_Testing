import pytest

from server import app, clubs


@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.mark.skipif(len(clubs) == 0, reason="Empty club list")
def test_known_email(client):
    email = clubs[0]['email']
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 200


def test_unknown_email(client):
    email = 'a@a.a'
    response = client.post('/showSummary', data={'email': email})
    assert response.status_code == 403
