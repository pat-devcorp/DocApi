from enum import Enum

from ...domain.identifier_handler import IdentifierHandler
from ...domain.model.reference import Reference
from ..audit_handler import AuditHandler
from ..BrokerProtocol import BrokerProtocol
from ..criteria import Criteria
from ..RepositoryProtocol import RepositoryProtocol


class ImageEvent(Enum):
    JPG = 0
    PNG = 1


# TODO: Rule to manager can not have in progress more than 4 Images
class ImageUseCase:
    def __init__(
        self,
        ref_write_uid: IdentifierHandler,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker
        self._f = list(Reference._fields)

    def add_audit_fields(self) -> None:
        self._f += AuditHandler._fields

    def fetch(self, limit: int) -> list[dict]:
        matching = Criteria(self._f)
        matching._limit(limit)

        return self._r.fetch(self._f, matching)

    def get_by_id(self, obj_id: IdentifierHandler) -> dict:
        return self._r.get_by_id(obj_id.value, self._f)
