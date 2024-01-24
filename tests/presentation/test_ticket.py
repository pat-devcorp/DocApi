import pytest

from src.domain.DomainError import DomainError
from src.domain.model.ticket import TicketInterface
from src.infrastructure.broker.MockBroker import MockBroker
from src.infrastructure.providers.User import getMock
from src.infrastructure.repositories.MockRepository import MockRepository
from src.presentation.controller.ticket import TicketController
from src.utils.ResponseHandler import ID_NOT_VALID, SCHEMA_NOT_MATCH


def getMockController():
    u = getMock()
    r = MockRepository()
    b = MockBroker()
    return TicketController(u, r, b)


def test_interface_with_out_parameters():
    tc = getMockController()

    with pytest.raises(TypeError) as excinfo:
        tc.create()
    with pytest.raises(TypeError) as excinfo:
        tc.update()
    with pytest.raises(TypeError) as excinfo:
        tc.delete()


def test_interface_invalid_params():
    tc = getMockController()

    obj_id = TicketInterface.getIdentifier()
    print(f"ID:{obj_id}")
    obj = TicketInterface.newTicket(obj_id, "ready")
    print(f"OBJECT:{obj}")
    invalid_obj = TicketInterface.badTicket()
    print(f"INVALID OBJECT:{invalid_obj}")

    # with pytest.raises(DomainError) as excinfo:
    #     tc.create(invalid_obj.ticketId, invalid_obj.description)
    # assert str(excinfo.value) == ID_NOT_VALID[1]

    # with pytest.raises(DomainError) as excinfo:
    #     tc.getById(invalid_obj.ticketId)
    # assert str(excinfo.value) == ID_NOT_VALID[1]

    # with pytest.raises(DomainError) as excinfo:
    #     tc.delete(invalid_obj.ticketId)
    # assert str(excinfo.value) == ID_NOT_VALID[1]

    # with pytest.raises(DomainError) as excinfo:
    #     tc.create(obj.ticketId, invalid_obj.description)
    # assert str(excinfo.value) == SCHEMA_NOT_MATCH[1]

    with pytest.raises(DomainError) as excinfo:
        tc.update(obj.ticketId, invalid_obj._asdict())
    assert str(excinfo.value) == SCHEMA_NOT_MATCH[1]
