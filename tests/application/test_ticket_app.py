import pytest

from src.application.audit_handler import AuditHandler
from src.application.use_case.ticket import TicketUseCase
from src.domain.model.ticket import TicketDomain
from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.broker.rabbitmq import RabbitmqClient
from src.infrastructure.mongo.repositories.ticket_mongo import TicketMongo
from src.infrastructure.services.User import get_mock


def get_use_case():
    my_config = Bootstrap()
    u = get_mock()
    r = TicketMongo(my_config["MONGO_SERVER"])
    b = RabbitmqClient(my_config["RABBITMQ_SERVER"])
    return TicketUseCase(u, r, b)


def test_application_ticket():
    ta = get_use_case()
    obj_id, obj, partial_obj = get_objs()

    ta.add_audit_fields()
    assert set(AuditHandler._fields).issubset(set(ta._f))
    assert ta.create(obj) is None
    assert ta.fetch(0) == list()
    assert ta.update(partial_obj) is None
    assert ta.get_by_id(obj_id) == dict()
    assert ta.delete(obj_id) is None
