from enum import Enum

from ...domain.model.person import Person, PersonId
from ..audit_handler import AuditHandler
from ..BrokerProtocol import BrokerProtocol
from ..RepositoryProtocol import RepositoryProtocol


class PersonEvent(Enum):
    CREATED = 0


class PersonUseCase:
    def __init__(
        self,
        ref_write_uid: PersonId,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker
        self._f = list(Person._fields)

    def add_audit_fields(self) -> None:
        self._f += AuditHandler._fields

    def get_by_id(self, person_id) -> dict:
        return self._r.get_by_id(person_id.value, self._f)
