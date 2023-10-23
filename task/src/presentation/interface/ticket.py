from collections import namedtuple

from ...domain.ticket import EnsureTicket
from .InterfaceError import InterfaceError

TicketDTO = namedtuple(
    "TicketDTO", ["write_uid", "ticket_id", "description", "category", "state"]
)

class Ticket:
    def _validateRequiredParams(params: dict):
        if params.get("write_uid") is None:
            raise InterfaceError("User must be provided")

        if params.get("ticket_id") is None:
            raise InterfaceError("Identifier must be provided")
    
    @classmethod
    def validateIdentity(ticket_id):
        domain_error = EnsureTicket.validateTicketId(ticket_id)
        if domain_error is not None:
            raise InterfaceError("Identifier must be provided")

    @classmethod
    def fromDict(cls, params: dict):
        cls._validateRequiredParams(params)

        ticket_dto = dict()
        for k in TicketDTO._fields:
            ticket_dto[k] = params[k] if params.get(k) is not None else None

        errors = EnsureTicket.partialValidate(ticket_dto)
        if len(errors) > 0:
            raise InterfaceError("\n".join(errors))

        return TicketDTO(**ticket_dto)
