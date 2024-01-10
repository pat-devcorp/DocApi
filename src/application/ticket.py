from enum import Enum
from typing import Protocol

from ..domain.IdentifierHandler import IdentifierHandler
from ..domain.model.ticket import TicketDomain, TicketDto, TicketDao, objIdentifier


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


class TicketRepositoryProtocol(Protocol):
    def fetch() -> list:
        pass

    def create() -> None:
        pass

    def update() -> None:
        pass

    def getById(objId) -> TicketDto:
        pass

    def delete(objId) -> None:
        pass


class TicketBrokerProtocol(Protocol):
    def pub(subject, data):
        pass


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
        return ref_repository.fetch(self._f)
    
    def getById(self, objId: TicketIdentifier) -> dict:
        return ref_repository.getById(objId, self._f)

    def delete(self, objId: TicketIdentifier) -> None:
        if self._r.entityExists(objId):
            raise ApplicationError(DB_GET_FAIL, "Entity ticket not exists")

        audit = AuditHandler.getUpdateFields(self._w)
        self.update(objId, audit)
        return self._r.delete(objId)

    def update(self, objId: TicketIdentifier, data) -> None:
        if ticket := self._r.getById(objId):
            raise ApplicationError(DB_GET_FAIL, "Entity ticket not exists")

        data.pop("ticketId")
        ticket.update(data)
        ticket.update(AuditHandler.getUpdateFields(self._w))
        return self._r.update(ticket)

    def create(self, obj: Ticket) -> None:
        ticket = obj.asDict()
        ticket.update(AuditHandler.getCreateFields(self._w))
        return self._r.create(ticket)