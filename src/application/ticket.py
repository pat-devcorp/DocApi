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
        self._c = TicketDomain(ref_write_uid, ref_repository)
        self._b = ref_broker

    def fetch(self) -> list:
        return self._c.fetch()

    def create(self, ticket_id: IdentifierHandler, description, category, state):
        obj_id = IdentityHandler(self._r, ticket_id)
        obj = TicketDAO(obj_id, description, category, state)
        return self._c.create(obj)

    def update(self, ticket_id: IdentifierHandler, description, category, state):
        obj_id = IdentityHandler(self._r, ticket_id)
        obj = TicketDAO(obj_id, description, category, state)
        return self._c.update(obj)

    def getByID(self, ticket_id: IdentifierHandler) -> list:
        obj_id = IdentityHandler(self._r, ticket_id)
        return self._c.getByID(obj_id)

    def delete(self, ticket_id: IdentifierHandler) -> bool:
        obj_id = IdentityHandler(self._r, ticket_id)
        return self._c.delete(obj_id)
