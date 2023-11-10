from ...utils.AuditHandler import AuditDTO
from ..dao.ticket import EnsureTicket
from ..RepositoryProtocol import RepositoryProtocol
from .BaseAudit import BaseAuditRepository


class TicketRepository(BaseAuditRepository):
    _name = "ticket"
    _id = "ticket_id"

    def __init__(self, ref_write_uid, ref_repository: RepositoryProtocol):
        self._write_uid = ref_write_uid
        self._repository = ref_repository
        self._fields = list(EnsureTicket.getFields()) + list(AuditDTO._fields)
        self._func_filter = EnsureTicket.domainFilter