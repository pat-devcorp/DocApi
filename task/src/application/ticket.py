from enum import Enum

from ..domain.controller.ticket import TicketRepository
from ..domain.RepositoryProtocol import RepositoryProtocol
from ..infraestructure.config import Config
from ..utils.IdentityHandler import IdentityHandler
from .BrokerProtocol import BrokerProtocol


class TicketEvent(Enum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3


class Ticket:
    def __init__(
        self,
        ref_write_uid: IdentityHandler,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._write_uid = ref_write_uid
        self._ticket = TicketRepository(ref_write_uid, ref_repository)
        self._broker = ref_broker

    @classmethod
    def entityExists(cls, ref_repository, identifier) -> bool:
        my_config = Config()
        ticket = TicketRepository(my_config.SYSTEM_UID, ref_repository)
        return ticket.entityExists(ref_repository, identifier)

    def fetch(self) -> list:
        return self._ticket.fetch()

    def create(self, params: dict):
        return self._ticket.create(params)

    def update(self, params: dict):
        return self._ticket.update(params)

    def getByID(self, identifier: IdentityHandler) -> list:
        return self._ticket.getByID(identifier)

    def delete(self, identifier: IdentityHandler) -> bool:
        return self._ticket.delete(identifier)
