import pytest

from src.domain.enum.channel_type import ChannelType
from src.domain.enum.ticket_status import TicketState
from src.domain.model.ticket import Ticket, TicketDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.ticket import TicketController

ticket_id = TicketDomain.get_default_identifier()
type_channel = ChannelType.MAIL
state = TicketState.END
ticket = {
    "requirement": "test",
    "because": "help with development",
}


def get_mock_controller():
    u = UserService.get_default_identifier()
    r = MockRepositoryClient(ticket)
    b = MockBrokerClient()
    return TicketController(u, r, b)


def test_new_ticket():
    assert hasattr(ticket_id, "value")
    obj = TicketDomain.new(ticket_id, type_channel, **ticket)
    assert isinstance(obj, Ticket)
    assert isinstance(TicketDomain.as_dict(obj), dict)


def test_new_ticket_adding_state():
    dct = dict(ticket)
    dct.update({"state": state.value})
    obj = TicketDomain.new(ticket_id, type_channel, **ticket)
    assert isinstance(obj, Ticket)


def test_update_ticket():
    dct = dict(ticket)
    dct.update({"ticket_id": ticket_id.value})
    obj = TicketDomain.from_dict(dct)
    assert isinstance(obj, Ticket)
