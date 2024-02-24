import pytest

from src.application.AuditHandler import AuditHandler
from src.application.ticket import TicketApplication
from src.domain.model.ticket import TicketDomain
from src.infrastructure.broker.MockBroker import MockBroker
from src.infrastructure.mongo.MockRepository import MockRepository
from src.infrastructure.services.User import get_mock


def get_mock_application():
    u = get_mock()
    r = MockRepository()
    b = MockBroker()
    return TicketApplication(u, r, b)


def get_objs():
    obj_id = TicketDomain.get_identifier()
    print(f"ID:{obj_id}")
    obj = TicketDomain.new_ticket(obj_id, "ready")
    print(f"OBJECT:{obj}")
    partial_obj = TicketDomain.partial_ticket(obj_id, {"description": "steady"})
    return obj_id, obj, partial_obj


def test_interface_with_out_parameters():
    ta = get_mock_application()

    with pytest.raises(TypeError) as error:
        ta.create()
    with pytest.raises(TypeError) as error:
        ta.update()
    with pytest.raises(TypeError) as error:
        ta.delete()


def test_application_ticket():
    ta = get_mock_application()
    obj_id, obj, partial_obj = get_objs()

    ta.add_audit_fields()
    assert set(AuditHandler._fields).issubset(set(ta._f))
    assert ta.create(obj) is None
    assert ta.fetch(0) == list()
    assert ta.update(partial_obj) is None
    assert ta.get_by_id(obj_id) == dict()
    assert ta.delete(obj_id) is None
