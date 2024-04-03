import pytest

from src.domain.DomainError import DomainError
from src.domain.enum.ticket_status import TicketState
from src.domain.enum.type_channel import TypeChannel
from src.domain.model.ticket import Ticket, TicketDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.ticket import TicketController


def get_mock_controller():
    u = UserService.get_default_identifier()
    obj = {
        "ticket_id": TicketDomain.get_default_identifier(),
        "type_channel": TypeChannel.MAIL.value,
        "requirement": "test",
        "because": "help with development",
        "state": TicketState.END.value,
    }
    r = MockRepositoryClient(obj)
    b = MockBrokerClient()
    return TicketController(u, r, b)


def test_domain():
    identifier = TicketDomain.get_default_identifier()
    assert hasattr(identifier, "value")
    valid_obj = {
        "type_channel": TypeChannel.MAIL,
        "requirement": "create a ticket",
        "because": "test the requirement",
    }
    defaults = {
        "state": TicketState.END,
    }
    obj_1 = TicketDomain.new(identifier, **valid_obj)
    assert isinstance(obj_1, Ticket)
    assert isinstance(TicketDomain.as_dict(obj_1), dict)
    obj_2 = TicketDomain.new(identifier, **valid_obj, **defaults)
    assert isinstance(obj_2, Ticket)
    dct = dict(valid_obj)
    dct.update({"ticket_id": identifier.value})
    obj_3 = TicketDomain.from_dict(dct)
    assert isinstance(obj_3, Ticket)
