from enum import Enum
from typing import Protocol

from ..domain.IdentifierHandler import IdentifierHandler
from ..domain.model.ticket import TicketDto, TicketDao, TicketIdentifier


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
        self._w = ref_write_uid
        self.r = ref_repository
        self._b = ref_broker

    def fetch(self) -> list:
        _d = TicketDao(self._w, self._r)
        return _d.fetch()

    def create(self, dto: TicketDto) -> None:
        _d = TicketDao(self._w, self._r)
        _d.create(dto)
        return self._b.pub(TicketEvent.CREATED, dto.ticketId)

    def update(self, dto: TicketDto) -> None:
        _d = TicketDao(self._w, self._r)
        _d.update(dto)

    def getById(self, ticketId: TicketIdentifier) -> TicketDto:
        _d = TicketDao(self._w, self._r)
        return _d.getById(ticketId)

    def delete(self, ticketId: TicketIdentifier) -> None:
        _d = TicketDao(self._w, self._r)
        return _d.delete(ticketId)
