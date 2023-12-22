from enum import Enum

from ..domain.controller.ticket import TicketDomain
from ..domain.dao.ticket import TicketCategory, TicketState, TicketTypeCommit
from ..domain.RepositoryProtocol import RepositoryProtocol
from ..presentation.IdentifierHandler import IdentifierHandler
from .BrokerProtocol import BrokerProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


class TicketApplication:
    def __init__(
        self,
        ref_write_uid: IdentifierHandler,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._write_uid = ref_write_uid
        self._r = ref_repository
        self._d = TicketDomain(ref_write_uid, ref_repository)
        self._b = ref_broker

    def fetch(self) -> list:
        return self._d.fetch()

    def create(
        self,
        ticketId: IdentifierHandler,
        description: str,
        category: TicketCategory,
        state: TicketState,
        typeCommit: TicketTypeCommit,
    ):
        return self._d.create(ticketId, description, category, state, typeCommit)

    def update(
        self,
        ticketId: IdentifierHandler,
        description: str = None,
        category: TicketCategory = None,
        state: TicketState = None,
        typeCommit: TicketTypeCommit = None,
    ):
        return self._d.update(ticketId, description, category, state, typeCommit)

    def getByID(self, ticketId: IdentifierHandler) -> list:
        return self._d.getByID(ticketId)

    def delete(self, ticketId: IdentifierHandler) -> bool:
        return self._d.delete(ticketId)
