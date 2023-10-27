from collections import namedtuple

from ...domain.ticket import EnsureTicket, TicketCategory, TicketState
from .InterfaceError import InterfaceError

TicketDTO = namedtuple("TicketDTO", ["ticket_id", "description", "category", "state"])


class Ticket:
    @classmethod
    def getMock():
        return TicketDTO(
            ticket_id = "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            description = "Test task",
            category = 0,
            state = 0,
        )
    
    @classmethod
    def getIdentifier(cls, ticket_id):
        return EnsureTicket.getIdentifier(ticket_id)

    @classmethod
    def fromDict(cls, params: dict):
        if params.get("ticket_id") is None:
            raise InterfaceError("Identifier must be provided")

        ticket = dict()
        for k in TicketDTO._fields:
            ticket[k] = params[k] if params.get(k) is not None else None

        errors = EnsureTicket.partialValidate(ticket)
        if len(errors) > 0:
            raise InterfaceError("\n".join(errors))

        return TicketDTO(**ticket)

    @classmethod
    def create(
        ticket_id,
        description,
        category=TicketCategory.DEFAULT,
        state=TicketState.CREATED,
    ):
        ticket_dto = TicketDTO(ticket_id, description, category, state)
        errors = EnsureTicket.partialValidate(ticket_dto)
        if len(errors) > 0:
            raise InterfaceError("\n".join(errors))
        return ticket_dto
