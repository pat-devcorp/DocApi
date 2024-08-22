from ...domain.identifier_handler import IdentifierHandler
from ...domain.model.person import Person, PersonDomain
from ...domain.model.status_code import DB_ID_NOT_FOUND, INVALID_FORMAT
from ..ApplicationError import ApplicationError
from ..audit_handler import AuditHandler
from ..BrokerProtocol import BrokerProtocol
from ..criteria import Criteria
from ..RepositoryProtocol import RepositoryProtocol


class PersonUseCase:
    def __init__(
        self,
        ref_write_uid: IdentifierHandler,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker
        self._f = list(Person._fields)

    def add_audit_fields(self) -> None:
        self._f += AuditHandler._fields

    def from_list(self, keys: list, data: list) -> Person:
        return [PersonDomain.from_dict(item) for item in zip(keys, data)]

    def fetch(self, limit: int) -> list[dict]:
        matching = Criteria(self._f)
        matching._limit(limit)

        return self._r.fetch(self._f, matching)

    def get_by_id(self, obj_id: IdentifierHandler) -> dict:
        return self._r.get_by_id(obj_id.value, self._f)

    def delete(self, obj_id: IdentifierHandler) -> None | ApplicationError:
        identifier = obj_id.person_id
        if not self._r.entity_exists(identifier):
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity not exists")

        return self._r.delete(identifier)

    def update(self, obj: Person) -> None | ApplicationError:
        identifier = obj.person_id
        if not self._r.entity_exists(identifier):
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity not exists")

        item = PersonDomain.as_dict(obj)
        item.update(AuditHandler.get_update_fields(self._w))

        return self._r.update(identifier, item)

    def create(self, obj: Person) -> None:
        item = PersonDomain.as_dict(obj)
        item.update(AuditHandler.get_create_fields(self._w))

        return self._r.create(item)

    def insert_many(self, data) -> None:
        errors = list()
        for idx, item in enumerate(data):
            try:
                PersonDomain.is_valid(item)
            except Exception as de:
                errors(f"{idx}: {str(de)}")
                continue

        if len(errors) > 0:
            raise ApplicationError(INVALID_FORMAT, "\n".join(errors))

        audit = AuditHandler.get_create_fields(self._w)
        for item in data:
            item.update(audit)

        return self._r.insert_many(data)
