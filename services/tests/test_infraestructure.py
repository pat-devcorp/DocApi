import pytest
from flask import Flask

from src.infraestructure.server import create_server


@pytest.fixture
def client():
    app = create_server()  # Create your Flask app
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome" in response.data
