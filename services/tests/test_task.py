from typing import List

from src.presentation.controller.ticket import Ticket as TicketController
from src.presentation.interface.ticket import Ticket as TicketInterface

# from src.struct.ticket import Ticket as TicketDomain


class RepositoryMock:
    def get(self, tablename: str, attrs: List[str]):
        return [{"ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"}]

    def getByID(self, tablename: str, pk: str, id_val: str, attrs: List[str]):
        return {"ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"}

    def update(self, tablename: str, pk: str, id_val: str, kwargs: dict):
        return {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            "description": "This is a ticket modified",
            "category": 0,
            "state": 0,
            "write_uid": "8888",
            "write_at": "2023-10-10 16:41:53",
            "create_uid": "9999",
            "create_at": "2023-10-10 16:41:53",
        }

    def create(self, tablename: str, kwargs: dict):
        return {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            "description": "This is a ticket modified",
            "category": 0,
            "state": 0,
            "write_uid": "7777",
            "write_at": "2023-10-10 16:41:53",
            "create_uid": "9999",
            "create_at": "2023-10-10 16:41:53",
        }


class ProducerMock:
    def send_message(self, topic: str, message: str) -> bool:
        print(f"Message sent to topic '{topic}': {message}")
        return True


def test_struct():
    test_ticket_dto = {
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        "write_uid": "999",
        "description": "This is a ticket",
    }
    my_ticket_dto = TicketInterface.fromDict(test_ticket_dto)
    my_repository = RepositoryMock()
    my_producer = ProducerMock()

    my_ticket_controller = TicketController(my_repository, my_producer)
    my_ticket_controller.create(my_ticket_dto)

    test_ticket_dto = {
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        "description": "This is a ticket modified",
        "category": 0,
        "state": 0,
        "write_uid": "8888",
        "write_at": "2023-10-10 16:41:53",
        "create_uid": "9999",
        "create_at": "2023-10-10 16:41:53",
    }
    my_ticket_updated_dto = TicketInterface.fromDict(test_ticket_dto)
    my_ticket_controller.update(my_ticket_updated_dto)

    print(my_ticket_controller)
    assert my_ticket_controller


# def test_controller():
#     my_ticket = TicketController(RepositoryMock())
#     my_ticket_dto = get_ticket()
#     response = my_ticket.create(**my_ticket_dto)
#     assert my_ticket_dto == response


# def test_struct():
#     ticket = TicketController(RepositoryMock())
#     my_dto = {"write_uid": "999", "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c", "description": "This is a ticket"}
#     my_obj = ticket.create(**my_dto)

#     assert my_obj == {"ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"}


# def test_application():
