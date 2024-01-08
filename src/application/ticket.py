from enum import Enum

from ..domain.controller.ticket import TicketDomain
from ..domain.dao.ticket import TicketCategory, TicketState, TicketTypeCommit
from ..presentation.IdentifierHandler import IdentifierHandler
from .BrokerProtocol import BrokerProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


class TicketRepositoryProtocol(Protocol):
    def fetch():
        pass

    def create(ticketId, description, category, state, typeCommit):
        pass

    def update(ticketId, description, category, state, typeCommit):
        pass
    
    def getById(ticketId):
        pass
    
    def delete(ticketId):
        pass


class TicketApplication:
    def __init__(
        self,
        ref_write_uid: IdentifierHandler,
        ref_repository: TicketRepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._w = ref_write_uid
        self._r = ref_repository
        self._b = ref_broker

    def fetch(self) -> list:
        return self._d.fetch()

    def create(
        self,
        dto: TicketDto
    ):
        _d = TicketDao(self._w, self._r, dto)
        return _d.create()

    def update(
        self,
        dto: TicketDto
    ):
        _d = TicketDao(self._w, self._r, dto)
        return self._d.update(ticketId, description, category, state, typeCommit)

    def getById(self, ticketId: TicketIdentifier) -> list:
        return TicketDao.getById(self._r, ticketId)

    def delete(self, ticketId: TicketIdentifier) -> bool:
        return TicketDao.delete(self._w, self._r, ticketId)
