import unittest

import pytest

from src.application.audit_handler import AuditHandler
from src.application.use_case.task import TaskUseCase
from src.domain.model.task import TaskDomain
from src.infrastructure.bootstrap.bootstrap import Bootstrap
from src.infrastructure.broker.rabbitmq import MyRabbitmqClient
from src.infrastructure.my_mongo.repositories.task_mongo import TaskMongo
from src.infrastructure.services.User import UserService


class TestTaskUseCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        my_config = Bootstrap()
        u = UserService.get_default_identifier()
        r = TaskMongo(my_config.REPOSITORY_MONGO, TaskDomain.pk)
        b = MyRabbitmqClient(my_config.BROKER_RABBITMQ)
        cls.use_case = TaskUseCase(u, r, b)
        cls.obj = TaskDomain.get_valid_task()
        cls.obj_id = TaskDomain.set_identifier(cls.obj.task_id)

    def test_application_task(self):
        self.use_case.add_audit_fields()
        assert set(AuditHandler._fields).issubset(set(self.use_case._f))
        assert self.use_case.create(self.obj) is None
        assert isinstance(self.use_case.fetch(0), list)
        assert self.use_case.update(self.obj) is None
        assert isinstance(self.use_case.get_by_id(self.obj_id), dict)
        assert self.use_case.delete(self.obj.task_id) is None
