from typing import Protocol

from ...domain.identifier_handler import IdentifierHandler
from ...domain.model.constant import (
    DB_CREATE_FAIL,
    DB_DELETE_FAIL,
    DB_ENTITY_NOT_FOUND,
    DB_GET_BY_PARAM_FAIL,
    DB_GET_FAIL,
    DB_UPDATE_FAIL,
)
from ...domain.model.task import Task, TaskDomain
from ..application_error import ApplicationError
from ..audit_handler import AuditHandler
from ..broker_protocol import BrokerProtocol
from ..infrastructure_error import InfrastructureError


class TaskRepositoryProtocol(Protocol):
    def entity_exists(identifier: str) -> bool: ...

    def fetch(fields: list) -> Task: ...

    def get_by_id(identifier: str, fields: list) -> Task: ...

    def delete(identifier: str) -> None: ...

    def update(identifier: str, item: Task) -> None: ...

    def create(item: Task) -> str: ...


class TaskUseCase:
    def __init__(
        self,
        ref_write_uid: IdentifierHandler,
        ref_repository: TaskRepositoryProtocol,
        ref_broker: BrokerProtocol,
    ) -> None:
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker
        self._f = list(Task._fields)

    def add_audit_fields(self) -> None:
        self._f += AuditHandler._fields

    def fetch(self, limit: int):
        try:
            return self._r.fetch(self._f)
        except Exception as err:
            raise InfrastructureError(DB_GET_FAIL, str(err))

    def get_by_id(self, identifier):
        try:
            return self._r.get_by_id(identifier, self._f)
        except Exception as err:
            raise InfrastructureError(DB_GET_BY_PARAM_FAIL, str(err))

    def delete(self, identifier):
        try:
            return self._r.delete(identifier)
        except Exception as err:
            raise InfrastructureError(DB_DELETE_FAIL, str(err))

    def update(self, item: dict):
        item.update(AuditHandler.get_update_fields(self._w))

        try:
            return self._r.update(item)
        except Exception as err:
            raise InfrastructureError(DB_UPDATE_FAIL, str(err))

    def create(self, obj: Task):
        item = TaskDomain.as_dict(obj)
        item.update(AuditHandler.get_create_fields(self._w))

        try:
            return self._r.create(item)
        except Exception as err:
            raise InfrastructureError(DB_CREATE_FAIL, str(err))
