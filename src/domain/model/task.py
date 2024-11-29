from collections import namedtuple
from typing import List

from ..custom_dict import CustomDict
from ..custom_string import CustomString
from ..domain_error import DomainError
from ..enum.commit_type import CommitType
from ..enum.identifier_algorithm import IdentifierAlgorithm
from ..enum.task_state import TaskState
from ..identifier_handler import IdentifierHandler
from .constant import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT

Task = namedtuple(
    "Task",
    [
        "taskId",
        "requirement",
        "milestones",
        "because",
        "state",
    ],
)


class TaskDomain:
    _algorithm = IdentifierAlgorithm.SONY_FLAKE
    pk = "taskId"

    @classmethod
    def get_default_identifier(cls):
        identifierHandler = IdentifierHandler(cls._algorithm)
        return identifierHandler.get_default_identifier()

    @staticmethod
    def as_dict(namedtuple_instance) -> dict:
        return dict(namedtuple_instance._asdict())

    @classmethod
    def from_dict(cls, identifier: str, data: dict) -> dict | DomainError:
        item = {k: v for k, v in data.items() if k in Task._fields}
        item.update({cls.pk: identifier})

        pivot = {k: item.get(k, None) for k in Task._fields}
        cls.is_valid(**pivot)

        return item

    @classmethod
    def is_valid(
        cls,
        taskId,
        requirement,
        milestones,
        because,
        state,
    ) -> Task | DomainError:
        errors = list()

        if requirement is not None:
            if CustomString.is_empty_string(requirement):
                errors.append("invalid requirement")

        if milestones is not None:
            if type(milestones) is not list:
                errors.append("incorrect type")
            if len(milestones) == 0:
                errors.append("there is no goal to achive")

        if because is not None:
            if CustomString.is_empty_string(because):
                errors.append("invalid because")

        if state is not None:
            is_ok, err = TaskState.has_value(state)
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

    @classmethod
    def new(
        cls,
        taskId: str,
        requirement: str,
        milestones: List[str],
        because: str,
        state: TaskState,
    ) -> Task | DomainError:
        cls.is_valid(taskId, requirement, milestones, because, state.value)

        return Task(taskId, requirement, milestones, because, state.value)
