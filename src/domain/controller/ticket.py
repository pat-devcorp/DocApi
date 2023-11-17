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

    def getByID(self, dao_id: IdentityHandler) -> list:
        return self._r.getByID(dao_id.value, self._fields)

    def delete(self, dao_id: IdentityHandler) -> bool:
        self._r.delete(dao_id.value)

    def create(self, dao: TicketDAO) -> bool:
        data = dao.toRepository()
        data.update(AuditHandler.getCreateFields(self._write_uid))

        return self._r.create(data)

    def update(self, dao: TicketDAO) -> bool:
        data = dao.toRepository()
        data.update(AuditHandler.getUpdateFields(self._write_uid))

        return self._r.update(dao.ticket_id.value, data)
