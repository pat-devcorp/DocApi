from ...utils.AuditHandler import AuditDTO
from ...utils.IdentityHandler import IdentityHandler
from ..dao.ticket import EnsureTicket
from ..RepositoryProtocol import RepositoryProtocol
from .BaseAudit import BaseAuditRepository


class TicketRepository:
    _name = "ticket"
    _pk = "ticket_id"

    def __init__(self, ref_write_uid, ref_repository: RepositoryProtocol):
        self._write_uid = ref_write_uid
        self._repository = ref_repository
        self._fields = list(EnsureTicket.getFields()) + list(AuditDTO._fields)
        self._base = BaseAuditRepository(
            self._name,
            self._pk,
            self._write_uid,
            self._repository,
            self._fields,
            EnsureTicket,
        )

    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in self.fields]
        self._base.setFields(self._fields)

    @classmethod
    def entityExists(cls, ref_repository, identifier: IdentityHandler) -> bool:
        return cls._base.entityExists(ref_repository, cls._name, cls._pk, identifier)

    def fetch(self) -> list:
        return self._base.fetch()

    def getByID(self, identifier: IdentityHandler) -> list:
        return self._base.getByID(identifier)

    def delete(self, identifier: IdentityHandler) -> bool:
        return self._base.delete(identifier)

    def create(self, params: dict) -> bool:
        return self._base.create(params)

    def update(self, params: dict) -> bool:
        return self._base.update(params)
