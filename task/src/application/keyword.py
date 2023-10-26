from ..domain.params import EnsureTicket, TicketState
from ..utils.AuditHandler import AuditDTO, AuditHandler
from ..utils.IdentityHandler import IdentityHandler
from .ApplicationError import ApplicationError
from .BrokerProtocol import BrokerProtocol
from .RepositoryProtocol import RepositoryProtocol


class Keyword:
    _name = "keywords"
    _id = "name"

    def __init__(
        self,
        ref_write_uid,
        ref_repository: RepositoryProtocol,
        ref_broker: BrokerProtocol,
    ):
        self._write_uid = ref_write_uid
        self._repository = ref_repository
        self._broker = ref_broker
        self._fields += list(EnsureTicket.getFields())

    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in self._fields]

    @classmethod
    def entityExists(cls, ref_repository, identifier) -> bool:
        return (
            True
            if ref_repository.getByID(cls._name, cls._id, identifier, cls._name) is None
            else False
        )

    def fetch(self) -> list:
        return self._repository.get(self._name, self._fields)

    def create(self, params: dict) -> bool:
        data = EnsureTicket.domainFilter(params)

        self._repository.create(self._name, data)
        return True

    def update(self, params: dict) -> bool:
        print("---UPDATE---")
        data = EnsureTicket.domainFilter(params)
        if not self.entityExists(data[self._id]):
            raise ApplicationError(["params does not exist"])

        self._repository.update(self._name, self._id, data[self._id], data)
        return True

    def getByID(self, identifier: IdentityHandler) -> list:
        return self._repository.getByID(self._name, self._id, identifier, self._fields)

    def delete(self, identifier) -> bool:
        if not self.entityExists(identifier):
            raise ApplicationError(["params does not exist"])

        self._repository.delete(self._name, self._id, identifier)

        return True
