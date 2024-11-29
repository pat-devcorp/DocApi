import unittest

import pytest

from src.domain.DomainError import DomainError
from src.domain.model.status_code import FIELD_REQUIRED, ID_NOT_VALID, INVALID_FORMAT
from src.domain.model.task import Task, TaskDomain
from src.infrastructure.broker.mock_broker import MockBrokerClient
from src.infrastructure.my_mongo.mock_repository import MockRepositoryClient
from src.infrastructure.services.User import UserService
from src.presentation.controller.task import TaskController


class TestTaskController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.task = TaskDomain.get_valid_task()
        cls.task_id = TaskDomain.set_identifier(cls.task.task_id)
        cls.invalid_task = TaskDomain.get_invalid_task()
        u = UserService.get_default_identifier()
        r = MockRepositoryClient(TaskDomain.as_dict(cls.task))
        b = MockBrokerClient()
        cls.controller = TaskController(u, r, b)

    def test_attrs(self):
        assert hasattr(self.task_id, "value")
        assert isinstance(TaskDomain.as_dict(self.task), dict)

    def test_new_task(self):
        obj = TaskDomain.new(
            self.task_id,
            self.task.channel_type,
            self.task.requirement,
            self.task.because,
            self.task.state,
        )
        assert isinstance(obj, Task)

    def test_new_task_adding_attrs(self):
        obj = TaskDomain.new(
            self.task_id,
            self.task.channel_type,
            self.task.requirement,
            self.task.because,
            self.task.state,
            self.task.attrs,
        )
        assert isinstance(obj, Task)

    def test_update_task(self):
        obj = TaskDomain.from_dict(TaskDomain.as_dict(self.task))
        assert isinstance(obj, Task)

    def test_interface_invalid_params(self):
        with pytest.raises(DomainError) as error:
            self.controller.create(
                None,
                self.invalid_task.channel_type,
                self.invalid_task.requirement,
                self.invalid_task.because,
                self.invalid_task.state,
                self.invalid_task.attrs,
            )
            assert error.code == FIELD_REQUIRED[0]

        with pytest.raises(DomainError) as error:
            self.controller.create(
                self.invalid_task.task_id,
                self.invalid_task.channel_type,
                self.invalid_task.requirement,
                self.invalid_task.because,
                self.invalid_task.state,
                self.invalid_task.attrs,
            )
            assert error.code == INVALID_FORMAT[0]


if __name__ == "__main__":
    unittest.main()
