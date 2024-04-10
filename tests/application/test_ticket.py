import unittest

import pytest

from src.application.audit_handler import AuditHandler
from src.application.use_case.ticket import TicketUseCase
from src.domain.model.ticket import TicketDomain
from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.broker.rabbitmq import RabbitmqClient
from src.infrastructure.mongo.repositories.ticket_mongo import TicketMongo
from src.infrastructure.services.User import UserService


class TestTicketUseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        my_config = Bootstrap()
        u = UserService.get_default_identifier()
        r = TicketMongo(my_config.REPOSITORY_MONGO, TicketDomain.pk)
        b = RabbitmqClient(my_config.BROKER_RABBITMQ)
        cls.use_case = TicketUseCase(u, r, b)
        cls.obj = TicketDomain.get_valid_ticket()
        cls.obj_id = TicketDomain.set_identifier(cls.obj.ticket_id)

    def test_application_ticket(self):
        self.use_case.add_audit_fields()
        assert set(AuditHandler._fields).issubset(set(self.use_case._f))
        assert self.use_case.create(self.obj) is None
        assert isinstance(self.use_case.fetch(0), list)
        assert self.use_case.update(self.obj) is None
        assert isinstance(self.use_case.get_by_id(self.obj_id), dict)
        assert self.use_case.delete(self.obj.ticket_id) is None
