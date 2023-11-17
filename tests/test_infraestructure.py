import pytest

from src.infraestructure.broker.kafka import Kafka
from src.infraestructure.repositories.ticket_mongo import Ticket
from src.infraestructure.server import createServer


@pytest.fixture
def client():
    app = createServer()
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hello" in response.data


def test_404_not_found(client):
    response = client.get("/nonexistent-page")
    assert response.status_code == 404
    assert b"404 Not Found" in response.data


def test_mongo_repository():
    mongo_repository = Ticket()
    assert (
        mongo_repository._mongo.chain_connection
        == "mongodb://mongo:mongo@localhost:27017/?authMechanism=DEFAULT"
    )
    fields = ["write_uid", "_id", "description"]
    current_id = "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"

    dto = {
        "write_uid": "8888",
        "ticket_id": current_id,
        "description": "This is a ticket modified",
    }
    if mongo_repository.getByID(current_id, ["description"]) is None:
        mongo_repository.create(dto)

    datos = mongo_repository.fetch(fields)
    assert datos

    text = "It was modified"
    mongo_repository.update(current_id, {"description": text})

    data = mongo_repository.getByID(current_id, ["description"])
    assert data["description"] == text


# def test_kafka_producer():
#     print("----KAFKA PROD")
#     kafka_producer = Kafka.setToDefault()
#     assert kafka_producer.chain_connection == "172.25.0.2:9092"
#     current_id = "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"

#     dto = {
#         "write_uid": "8888",
#         "_id": current_id,
#         "description": "This is a ticket modified",
#     }
#     try:
#         kafka_producer.sendMessage("create/task", str(dto))
#         assert True
#     except Exception as e:
#         assert False
