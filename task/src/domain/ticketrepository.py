from ..utils.AuditHandler import AuditDTO, AuditHandler
from ..utils.IdentityHandler import IdentityHandler
from .DomainError import DomainError
from .RepositoryProtocol import RepositoryProtocol
from .ticket import EnsureTicket, TicketState


class TicketRepository:
    _name = "ticket"
    _id = "ticket_id"

    def __init__(self, ref_write_uid, ref_repository: RepositoryProtocol):
        self._write_uid = ref_write_uid
        self._repository = ref_repository
        self._fields += list(EnsureTicket.getFields()) + list(AuditDTO._fields)

    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in self._fields]

    @classmethod
    def entityExists(cls, ref_repository, identifier) -> bool:
        return (
            True
            if ref_repository.getByID(cls._name, cls._id, identifier, cls._id) is None
            else False
        )

    def fetch(self) -> list:
        return self._repository.get(self._name, self._fields)

    def create(self, params: dict) -> bool:
        data = EnsureTicket.domainFilter(params)
        my_audit = AuditHandler.create(self._write_uid)
        my_ticket = my_audit._asdict() | data

        self._repository.create(self._name, my_ticket)
        return True

    def update(self, params: dict) -> bool:
        print("---UPDATE---")
        data = EnsureTicket.domainFilter(params)
        if not self.entityExists(data[self._id]):
            raise DomainError(["params does not exist"])

        my_audit = AuditHandler.getUpdateFields(self._write_uid)
        data.update(my_audit)

        self._repository.update(self._name, self._id, data[self._id], data)
        return True

    def getByID(self, identifier: IdentityHandler) -> list:
        return self._repository.getByID(self._name, self._id, identifier, self._fields)

    def delete(self, identifier: IdentityHandler) -> bool:
        if not self.entityExists(identifier):
            raise DomainError(["params does not exist"])

        my_audit = AuditHandler.getUpdateFields(self._write_uid)
        my_audit.update({"state": TicketState.DELETED})

        self._repository.update(self._name, self._id, identifier, my_audit)
        return True
