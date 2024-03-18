from enum import Enum

from ...domain.identifier_handler import Identifier
from ...domain.model.ticket import PartialTicket, Ticket, TicketDomain, TicketIdentifier
from ...utils.response_code import DB_ID_NOT_FOUND
from ..ApplicationError import ApplicationError
from ..audit_handler import AuditHandler
from ..BrokerProtocol import BrokerProtocol
from ..criteria import Criteria
from ..RepositoryProtocol import RepositoryProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


# TODO: Rule to manager can not have in progress more than 4 tickets
class TicketUseCase:
    def __init__(
        self,
        ref_write_uid: Identifier,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker
        self._f = list(Ticket._fields)

    def add_audit_fields(self) -> None:
        self._f += AuditHandler._fields

    def from_list(self, keys: list, data: list) -> Ticket | PartialTicket:
        return [TicketDomain.from_repo(item) for item in zip(keys, data)]

    def fetch(self, limit: int) -> list[dict]:
        matching = Criteria(self._f)
        matching._limit(limit)

        return self._r.fetch(self._f, matching)

    def get_by_id(self, obj_id: TicketIdentifier) -> dict:
        return self._r.get_by_id(obj_id.value, self._f)

    def delete(self, obj_id: TicketIdentifier) -> None | ApplicationError:
        if not self._r.entity_exists(obj_id):
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity ticket not exists")

        audit = AuditHandler.get_update_fields(self._w)
        data = TicketDomain.from_dict(obj_id, audit)
        self.update(data)

        return self._r.delete(obj_id.value)

    def update(self, obj: Ticket | PartialTicket) -> None | ApplicationError:
        identifier = obj.ticketId
        if not self._r.entity_exists(identifier):
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity ticket not exists")

        item = TicketDomain.as_dict(obj)
        item.update(AuditHandler.get_update_fields(self._w))

        return self._r.update(identifier, item)

    def create(self, obj: Ticket) -> None:
        item = TicketDomain.as_dict(obj)
        item.update(AuditHandler.get_create_fields(self._w))

        return self._r.create(item)
