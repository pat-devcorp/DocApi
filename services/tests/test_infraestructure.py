import pytest

from src.infraestructure.server import createServer


@pytest.fixture
def client():
    app = createServer()  # Create your Flask app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data

def test_404_not_found(client):
    response = client.get('/nonexistent-page')
    assert response.status_code == 404
    assert b'404 Not Found' in response.data
