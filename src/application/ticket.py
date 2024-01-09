from enum import Enum
from typing import Protocol

from ..domain.IdentifierHandler import IdentifierHandler
from ..domain.model.ticket import TicketDomain, TicketDto, TicketDao, TicketIdentifier


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

    def getById(ticketId) -> TicketDto:
        pass

    def delete(ticketId) -> None:
        pass


class TicketBrokerProtocol(Protocol):
    def pub(subject, data):
        pass


class TicketApplication:
    def __init__(
        self,
        ref_write_uid: IdentifierHandler,
        ref_repository: TicketRepositoryProtocol,
        ref_broker: TicketBrokerProtocol,
    ):
        self._td = TicketDomain(ref_write_uid, ref_repository)
        self._b = ref_broker

    def fetch(self) -> list:
        return self._td.fetch()
    
    def getById(self, ticketId: TicketIdentifier) -> TicketDto:
        return self._td.getById(ticketId)

    def delete(self, ticketId: TicketIdentifier) -> None:
        return self._td.delete(ticketId)

    def update(self, obj) -> None:
        pass

    def create(self, obj) -> None:
        pass