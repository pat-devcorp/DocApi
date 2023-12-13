from ...utils.AuditHandler import AuditHandler
from ..dao.ticket import TicketDAO
from ..IdentityHandler import IdentityHandler
from ..RepositoryProtocol import RepositoryProtocol


class Ticket:
    def __init__(self, ref_write_uid, ref_repository: RepositoryProtocol):
        self._write_uid = ref_write_uid
        self._r = ref_repository
        self._fields = list(TicketDAO.getFields()) + list(AuditHandler.getFields())

    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in TicketDAO.getFields()]

    def fetch(self) -> list:
        return self._r.fetch(self._fields)

    def getByID(self, daoId: IdentityHandler) -> list:
        return self._r.getByID(daoId.value, self._fields)

    def delete(self, daoId: IdentityHandler) -> bool:
        self._r.delete(daoId.value)

    def create(self, dao: TicketDAO) -> bool:
        data = dao.asDict()
        data.update(AuditHandler.getCreateFields(self._write_uid))

        return self._r.create(data)

    def update(self, dao: TicketDAO) -> bool:
        data = dao.asDict()
        data.update(AuditHandler.getUpdateFields(self._write_uid))

        return self._r.update(data)
