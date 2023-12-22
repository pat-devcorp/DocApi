from ...utils.AuditHandler import AuditHandler
from ..dao.ticket import TicketDAO
from ..IdentityHandler import IdentityHandler
from ..RepositoryProtocol import RepositoryProtocol


class TicketDomain:
    def __init__(self, ref_write_uid, ref_repository: RepositoryProtocol):
        self._write_uid = ref_write_uid
        self._r = ref_repository
        self._fields = list(TicketDAO.getFields()) + list(AuditHandler.getFields())

    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in TicketDAO.getFields()]

    def prepareIdentity(self, identifier) -> IdentityHandler | DomainError:
        return IdentityHandler.ensureIdentity(self._r, identifier)

    def fetch(self) -> list:
        return self._r.fetch(self._fields)

    def create(
        self,
        ticketId: IdentifierHandler,
        description: str,
        category: TicketCategory,
        state: TicketState,
        typeCommit: TicketTypeCommit
    ):
        objId = IdentityHandler.create(ticketId)
        obj = TicketDAO(objId, description, category, state, typeCommit)
        return self.doCreate(obj)
    
    def update(
        self,
        ticketId: IdentifierHandler,
        description: str = None,
        category: TicketCategory = None,
        state: TicketState = None,
        typeCommit: TicketTypeCommit = None,
    ):
        objId = IdentityHandler.create(ticketId)
        obj = TicketDAO.updatedObj(objId, description, category, state, typeCommit)
        return self.doUpdate(obj)

    def getByID(self, ticket_id):
        objId = self.prepareIdentity(ticketId)
        return self.doGetByID(objId)
    
    def delete(self, ticket_id):
        objId = self.prepareIdentity(ticketId)
        return self.doDelete(objId)


    def doGetByID(self, daoId: IdentityHandler) -> list:
        return self._r.getByID(daoId.value, self._fields)

    def doDelete(self, daoId: IdentityHandler) -> bool:
        self._r.delete(daoId.value)

    def doCreate(self, dao: TicketDAO) -> bool:
        data = dao.asDict()
        data.update(AuditHandler.getCreateFields(self._write_uid))

        return self._r.create(data)

    def doUpdate(self, dao: TicketDAO) -> bool:
        data = dao.asDict()
        data.update(AuditHandler.getUpdateFields(self._write_uid))

        return self._r.update(data)
