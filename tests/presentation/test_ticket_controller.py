import pytest

from src.domain.DomainError import DomainError
from src.domain.enum.ticket_status import TicketState, TicketStatus
from src.domain.identifier_handler import IdentifierHandler
from src.domain.model.ticket import Ticket, TicketDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.ticket import TicketController
from utils.status_code import ID_NOT_VALID, SCHEMA_NOT_MATCH


class MockRepositoryClient:
    obj = {
        "ticket_id": IdentifierHandler.get_uuid_v4(),
        "channel_id": IdentifierHandler.get_uuid_v4(),
        "requirement": "test",
        "because": "help with development",
        "state": TicketStatus.END.value,
    }

    def dsn(self):
        return "mock-repos"

    def fetch(self, attrs, matching):
        return [self.obj]

    def get_by_id(self, identifier, attrs):
        return self.obj

    def delete(self, identifier) -> None:
        return None

    def update(self, identifier, kwargs) -> None:
        return None

    def create(self, kwargs) -> None:
        return None

    def insert_many(self, data) -> None:
        return None


def get_mock_controller():
    u = UserService.get_default_identifier()
    r = MockRepositoryClient()
    b = MockBrokerClient()
    return TicketController(u, r, b)


def test_domain():
    identifier = TicketDomain.get_default_identifier()
    channel_id = ChannelDomain.get_default_identifier()
    assert hasattr(identifier, "value")
    valid_obj = {
        "requirement": "create a ticket",
        "because": "test the requirement",
    }
    defaults = {
        "state": TicketState.END.value,
    }
    obj_1 = TicketDomain.new(identifier, channel_id, **valid_obj)
    assert isinstance(obj_1, Ticket)
    assert isinstance(TicketDomain.as_dict(obj_1), dict)
    obj_2 = TicketDomain.new(identifier, channel_id, **valid_obj, **defaults)
    assert isinstance(obj_2, Ticket)
    dct = dict(valid_obj)
    dct.update({"ticket_id": identifier.value})
    obj_3 = TicketDomain.from_dict(dct)
    assert isinstance(obj_3, Ticket)
