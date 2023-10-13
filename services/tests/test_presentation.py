from typing import List

from src.presentation.controller.ticket import Ticket as TicketController
from src.presentation.interface.InterfaceError import InterfaceError
from src.presentation.interface.ticket import Ticket as TicketInterface
from src.presentation.interface.ticket import TicketDTO

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
            "category": 1,
            "state": 1,
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
    def sendMessage(self, topic: str, message: str) -> bool:
        print(f"Message sent to topic '{topic}': {message}")
        return True


def test_interface_user_required():
    try:
        test_ticket_dto = {
            "write_uid": "9999",
        }
        TicketInterface.fromDict(test_ticket_dto)
        assert False
    except InterfaceError:
        assert True


def test_interface_id_required():
    try:
        test_ticket_dto = {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        }
        TicketInterface.fromDict(test_ticket_dto)
        assert False
    except InterfaceError:
        assert True


def assert_type_dto():
    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_dto = TicketInterface.fromDict(test_ticket_dto)
    assert isinstance(my_ticket_dto, TicketDTO)


def test_controller_create():
    my_repository = RepositoryMock()
    my_producer = ProducerMock()
    my_ticket_controller = TicketController(my_repository, my_producer)

    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        "description": "This is a ticket",
    }
    my_ticket_create_dto = TicketInterface.fromDict(test_ticket_dto)
    response_create = my_ticket_controller.create(my_ticket_create_dto)
    assert response_create


def test_controller_get():
    my_repository = RepositoryMock()
    my_producer = ProducerMock()
    my_ticket_controller = TicketController(my_repository, my_producer)

    response_get = my_ticket_controller.get()
    assert isinstance(response_get, list)


def test_controller_update():
    my_repository = RepositoryMock()
    my_producer = ProducerMock()
    my_ticket_controller = TicketController(my_repository, my_producer)

    test_ticket_dto = {
        "write_uid": "8888",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
        "description": "This is a ticket modified",
    }
    my_ticket_update_dto = TicketInterface.fromDict(test_ticket_dto)
    response_update = my_ticket_controller.update(my_ticket_update_dto)
    assert response_update


def test_controller_get_by_id():
    my_repository = RepositoryMock()
    my_producer = ProducerMock()
    my_ticket_controller = TicketController(my_repository, my_producer)

    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_get_dto = TicketInterface.fromDict(test_ticket_dto)
    response_get_by_id = my_ticket_controller.getByID(my_ticket_get_dto)
    assert isinstance(response_get_by_id, dict)


def test_controller_delete():
    my_repository = RepositoryMock()
    my_producer = ProducerMock()
    my_ticket_controller = TicketController(my_repository, my_producer)

    test_ticket_dto = {
        "write_uid": "9999",
        "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
    }
    my_ticket_delete_dto = TicketInterface.fromDict(test_ticket_dto)
    response_delete = my_ticket_controller.delete(my_ticket_delete_dto)
    assert response_delete
