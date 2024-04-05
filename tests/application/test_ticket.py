import unittest

import pytest

from src.application.audit_handler import AuditHandler
from src.application.use_case.ticket import TicketUseCase
from src.domain.model.ticket import TicketDomain
from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.broker.rabbitmq import RabbitmqClient
from src.infrastructure.mongo.repositories.ticket_mongo import TicketMongo
from src.infrastructure.services.User import get_mock


class TestTicketUseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        my_config = Bootstrap()
        u = get_mock()
        r = TicketMongo(my_config["MONGO_SERVER"])
        b = RabbitmqClient(my_config["RABBITMQ_SERVER"])
        cls.use_case = TicketUseCase(u, r, b)

    def test_application_ticket(self):
        self.use_case.add_audit_fields()
        assert set(AuditHandler._fields).issubset(set(ta._f))
        assert self.use_case.create(obj) is None
        assert self.use_case.fetch(0) == list()
        assert self.use_case.update(partial_obj) is None
        assert self.use_case.get_by_id(obj_id) == dict()
        assert self.use_case.delete(obj_id) is None
