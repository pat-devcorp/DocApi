import pytest

from src.domain.DomainError import DomainError
from src.domain.model.ticket import TicketDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.ticket import TicketController
from utils.status_code import ID_NOT_VALID, SCHEMA_NOT_MATCH


class MockRepositoryClient:
    object = {}

    def dsn(self):
        return "mock-repos"

    def fetch(self, attrs, matching):
        return [self.object]

    def get_by_id(self, identifier, attrs):
        return self.object

    def delete(self, identifier) -> None:
        return None

    def update(self, identifier, kwargs) -> None:
        return None

    def delete(self, kwargs) -> None:
        return None


def get_mock_controller():
    u = UserService.get_default_identifier()
    r = MockRepositoryClient()
    b = MockBrokerClient()
    return TicketController(u, r, b)


def test_domain():
    ticket_id = TicketDomain.get_default_identifier()
    print(f"ID:{TicketDomain.as_dict(ticket_id)}")
    ticket_1 = TicketDomain.new(
        ticket_id,
    )
    data_1 = TicketDomain.as_dict(ticket_1)
    print(f"OBJECT:{data_1}")
    attrs = {
        "birthDate": "1995/07/18",
        "documentNumber": "72539751",
        "address": "Cultura chimu 413",
    }
    ticket_2 = TicketDomain.new(
        ticket_id,
    )
    print(f"OBJECT:{TicketDomain.as_dict(ticket_2)}")
    ticket = {
        "ticketId": ticket_id.value,
        "name": "Patrick Alonso",
        "lastname": "Fuentes Carpio",
        "mailAddress": "patrick18483@gmail.com",
        "address": "Cultura chimu 413",
    }
    ticket_3 = TicketDomain.from_dict(ticket)
    print(f"OBJECT:{TicketDomain.as_dict(ticket_3)}")


# def get_invalid_obj():
#     return Ticket(
#         "a",
#         "a" * 201,
#         100,
#         100,
#         100,
#         100,
#         "20/20/20",
#     )


# def test_interface_with_out_parameters():
#     tc = get_mock_controller()

#     with pytest.raises(TypeError) as error:
#         tc.create()
#     with pytest.raises(TypeError) as error:
#         tc.update()
#     with pytest.raises(TypeError) as error:
#         tc.delete()


# def test_interface_invalid_params():
#     tc = get_mock_controller()
#     obj = get_obj()
#     invalid_obj = get_invalid_obj()

#     with pytest.raises(DomainError) as error:
#         tc.create(invalid_obj.ticketId, invalid_obj.requirement)
#     assert str(error.value) == ID_NOT_VALID[1]

#     with pytest.raises(DomainError) as error:
#         tc.get_by_id(invalid_obj.ticketId)
#     assert str(error.value) == ID_NOT_VALID[1]

#     with pytest.raises(DomainError) as error:
#         tc.delete(invalid_obj.ticketId)
#     assert str(error.value) == ID_NOT_VALID[1]

#     with pytest.raises(DomainError) as error:
#         tc.create(obj.ticketId, invalid_obj.requirement)
#     assert str(error.value) == SCHEMA_NOT_MATCH[1]

#     with pytest.raises(DomainError) as error:
#         tc.update(obj.ticketId, invalid_obj._asdict())
#     assert str(error.value) == SCHEMA_NOT_MATCH[1]
