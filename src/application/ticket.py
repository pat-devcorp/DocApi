from enum import Enum

from ..domain.controller.ticket import Ticket as TicketDomain
from ..domain.dao.ticket import TicketDAO
from ..domain.IdentityHandler import IdentityHandler
from ..domain.RepositoryProtocol import RepositoryProtocol
from ..presentation.IdentifierHandler import IdentifierHandler
from .BrokerProtocol import BrokerProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


class Ticket:
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
        category,
        state,
        typeCommit,
    ):
        objId = IdentityHandler.create(ticketId)
        obj = TicketDAO(objId, description, category, state, typeCommit)
        return self._d.create(obj)

    def update(
        self,
        ticketId: IdentifierHandler,
        description: str,
        category,
        state,
        typeCommit,
    ):
        objId = IdentityHandler.ensureIdentity(self._r, ticketId)
        obj = TicketDAO(objId, description, category, state, typeCommit)
        return self._d.update(obj)

    def getByID(self, ticketId: IdentifierHandler) -> list:
        objId = IdentityHandler.ensureIdentity(self._r, ticketId)
        return self._d.getByID(objId)

    def delete(self, ticketId: IdentifierHandler) -> bool:
        objId = IdentityHandler.ensureIdentity(self._r, ticketId)
        return self._d.delete(objId)
