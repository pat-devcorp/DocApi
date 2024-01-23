import pytest

from src.presentation.PresentationError import PresentationError
from src.infrastructure.providers.User import getMock
from src.infrastructure.repositories.MockRepository import MockRepository
from src.infrastructure.broker.MockBroker import MockBroker
from src.presentation.controller.ticket import TicketController


def test_interface():
    u = getMock()
    r = MockRepository()
    b = MockBroker()
    tc = TicketController(u, r, b)

    ticketId = "test"

    with pytest.raises(PresentationError) as err:
        tc.create(ticketId, "test")
    assert str(err.value) == ID_NOT_VALID[1]
    tc.fetch()
    tc.update(ticketId, "testing...")
    tc.getById(ticketId)
    tc.delete(ticketId)