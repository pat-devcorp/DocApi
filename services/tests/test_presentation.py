from typing import Dict, List

from src.presentation.controllers.ticket import Ticket as TicketController


class RepositoryMock:
    def get(self, tablename: str, attrs: List[str]):
        return [{"id": "1234567890"}]

    def get_by_id(self, tablename: str, pk: str, id_val: str, attrs: List[str]):
        return {"id": "1234567890"}

    def update(self, tablename: str, pk: str, id_val: str, kwargs: dict):
        return {
            "id": "1234567890",
            "write_uid": "1234567890",
            "description": "This is a ticket modified",
        }

    def create(self, tablename: str, kwargs: dict):
        return {
            "id": "1234567890",
            "write_uid": "1234567890",
            "description": "This is a ticket",
        }


def test_get():
    ticket = TicketController(RepositoryMock())
    datos = ticket.get_by_id("1234567890")

    assert datos == {"id": "1234567890"}


def test_create():
    ticket = TicketController(RepositoryMock())
    my_dto = {"write_uid": "1234567890", "description": "This is a ticket"}
    my_obj = ticket.create(**my_dto)

    assert my_obj == {"id": "1234567890"}


# def test_update():
#    ticket = TicketController(RepositoryMock())
#    my_dto = {
#        "write_uid": "1234567890",
#        "description": "This is a ticket modified",
#    }
#    my_obj = ticket.update(**my_dto)
#
#    assert my_obj == {"id": "1234567890"}
