import pytest

from src.domain.model.ticket import TicketDao
from src.infrastructure.broker.kafka import Kafka
from src.infrastructure.repositories.mongo import Mongo
from src.web.server import createServer


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
    mongo_repository = Mongo.setToDefault()
    print(f"CONNECTION: {mongo_repository.chain_connection}")
    current_id = "87378a1e-894c-11ee-b9d1-0242ac120002"

    dto = {
        "write_uid": "8888",
        "identifier": current_id,
        "description": "This is description",
    }
    mongo_repository.create("test", "identifier", dto)

    data = mongo_repository.fetch("test", "identifier", dto.keys())
    assert data

    text = "It was modified"
    mongo_repository.update("test", "identifier", current_id, {"description": text})

    data = mongo_repository.getById("test", "identifier", current_id, ["description"])
    assert data["description"] == text

    mongo_repository.delete("test", "identifier", current_id)
    assert (
        mongo_repository.getById("test", "identifier", current_id, ["description"])
        == None
    )


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
