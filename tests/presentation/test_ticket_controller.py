import pytest

from src.domain.DomainError import DomainError
from src.domain.model.ticket import TicketDomain
from src.infrastructure.broker.MockBroker import MockBroker
from src.infrastructure.mongo.MockRepository import MockRepository
from src.infrastructure.services.User import get_mock
from src.presentation.controller.ticket import TicketController
from src.utils.response_code import ID_NOT_VALID, SCHEMA_NOT_MATCH


def get_mock_controller():
    u = get_mock()
    r = MockRepository()
    b = MockBroker()
    return TicketController(u, r, b)


def get_obj():
    obj_id = TicketDomain.get_identifier()
    print(f"ID:{obj_id}")
    obj = TicketDomain.new_ticket(obj_id, "ready")
    print(f"OBJECT:{obj}")
    return obj


def get_invalid_obj():
    invalid_obj = TicketDomain.bad_ticket()
    print(f"INVALID OBJECT:{invalid_obj}")
    return invalid_obj


def test_interface_with_out_parameters():
    tc = get_mock_controller()

    with pytest.raises(TypeError) as error:
        tc.create()
    with pytest.raises(TypeError) as error:
        tc.update()
    with pytest.raises(TypeError) as error:
        tc.delete()


def test_interface_invalid_params():
    tc = get_mock_controller()
    obj = get_obj()
    invalid_obj = get_invalid_obj()

    with pytest.raises(DomainError) as error:
        tc.create(invalid_obj.ticketId, invalid_obj.description)
    assert str(error.value) == ID_NOT_VALID[1]

    with pytest.raises(DomainError) as error:
        tc.get_by_id(invalid_obj.ticketId)
    assert str(error.value) == ID_NOT_VALID[1]

    with pytest.raises(DomainError) as error:
        tc.delete(invalid_obj.ticketId)
    assert str(error.value) == ID_NOT_VALID[1]

    with pytest.raises(DomainError) as error:
        tc.create(obj.ticketId, invalid_obj.description)
    assert str(error.value) == SCHEMA_NOT_MATCH[1]

    with pytest.raises(DomainError) as error:
        tc.update(obj.ticketId, invalid_obj._asdict())
    assert str(error.value) == SCHEMA_NOT_MATCH[1]
