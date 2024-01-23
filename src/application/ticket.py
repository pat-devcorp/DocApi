from enum import Enum
from typing import Protocol

from ..domain.IdentifierHandler import IdentifierHandler
from ..domain.model.ticket import Ticket, TicketIdentifier
from ..utils.ResponseHandler import DB_ID_NOT_FOUND
from .ApplicationError import ApplicationError
from .AuditHandler import AuditHandler


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


class TicketRepositoryProtocol(Protocol):
    def fetch() -> list:
        pass

    def getById(objId) -> dict:
        pass

    def delete(objId) -> None:
        pass

    def update() -> None:
        pass

    def create() -> None:
        pass


class TicketBrokerProtocol(Protocol):
    def publish(subject, data):
        pass


# TODO: Rule to manager can not have in progress more than 4 tickets
class TicketApplication:
    def __init__(
        self,
        ref_writeUId: IdentifierHandler,
        ref_repository: TicketRepositoryProtocol,
        ref_broker: TicketBrokerProtocol,
    ):
        self._w = ref_writeUId
        self._r = ref_repository
        self._b = ref_broker
        self._f = Ticket.getFields()

    def addAuditFields(self):
        self._f += AuditHandler.getFields()

    def fetch(self) -> list[dict]:
        return self._r.fetch(self._f)

    def getById(self, objId: TicketIdentifier) -> dict:
        return self._r.getById(objId, self._f)

    def delete(self, objId: TicketIdentifier) -> None:
        if self._r.entityExists(objId):
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity ticket not exists")

        audit = AuditHandler.getUpdateFields(self._w)
        self.update(objId, audit)

        return self._r.delete(objId)

    def update(self, objId: TicketIdentifier, data) -> None:
        if (ticket := self._r.getById(objId)) is None:
            raise ApplicationError(DB_ID_NOT_FOUND, "Entity ticket not exists")

        data.pop("ticketId")
        ticket.update(data)
        ticket.update(AuditHandler.getUpdateFields(self._w))

        return self._r.update(ticket)

    def create(self, obj: Ticket) -> None:
        ticket = obj.asDict()
        ticket.update(AuditHandler.getCreateFields(self._w))

        return self._r.create(ticket)
