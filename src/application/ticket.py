from enum import Enum
from typing import Protocol

from ..domain.IdentifierHandler import IdentifierHandler
from ..domain.model.ticket import Ticket, TicketIdentifier, TicketInterface
from ..presentation.RepositoryProtocol import RepositoryProtocol
from ..utils.ResponseHandler import DB_ID_NOT_FOUND
from .ApplicationError import ApplicationError
from .AuditHandler import AuditHandler


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


class TicketBrokerProtocol(Protocol):
    def publish(subject, data):
        pass


# TODO: Rule to manager can not have in progress more than 4 tickets
class TicketApplication:
    def __init__(
        self,
        ref_writeUId: IdentifierHandler,
        ref_repository: RepositoryProtocol,
        ref_broker: TicketBrokerProtocol,
    ):
        self._w = ref_writeUId
        self._r = ref_repository
        self._b = ref_broker
        self._f = Ticket._fields

    def addAuditFields(self):
        self._f += AuditHandler._fields

    def fetch(self) -> list[dict]:
        return self._r.fetch(self._f)

    def getById(self, obj_id: TicketIdentifier) -> dict:
        return self._r.getById(obj_id.value, self._f)

    def delete(self, obj_id: TicketIdentifier) -> None:
        if not self._r.entityExists(obj_id):
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity ticket not exists")

        audit = AuditHandler.getUpdateFields(self._w)
        self.update(obj_id, audit)

        return self._r.delete(obj_id.value)

    def update(self, obj_id: TicketIdentifier, data: dict) -> None:
        if not self._r.entityExists(obj_id.value):
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity ticket not exists")

        item = TicketInterface.validDict(data)
        item = AuditHandler.getUpdateFields(self._w)

        return self._r.update(obj_id.value, item)

    def create(self, obj: Ticket) -> None:
        ticket = obj._asdict()
        ticket.update(AuditHandler.getCreateFields(self._w))

        return self._r.create(ticket)
