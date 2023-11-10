from collections import namedtuple

from ...utils.ErrorHandler import ID_NOT_FOUND
from ...domain.dao.ticket import EnsureTicket, TicketCategory, TicketState
from ..PresentationError import PresentationError

TicketDTO = namedtuple("TicketDTO", ["ticket_id", "description", "category", "state"])


class TicketHandler:
    @staticmethod
    def getMock():
        return TicketDTO(
            ticket_id="3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            description="Test task",
            category=0,
            state=0,
        )

    @staticmethod
    def getIdentifier(ticket_id):
        return EnsureTicket.getIdentifier(ticket_id)

    @staticmethod
    def fromDict(params: dict):
        if params.get("ticket_id") is None:
            raise PresentationError(ID_NOT_FOUND)

        ticket = dict()
        for k in TicketDTO._fields:
            ticket[k] = params[k] if params.get(k) is not None else None

        errors = EnsureTicket.partialValidate(ticket)
        if len(errors) > 0:
            raise PresentationError("\n".join(errors))

        return TicketDTO(**ticket)

    @staticmethod
    def create(
        ticket_id,
        description,
        category:int|TicketCategory=TicketCategory.UNDEFINED,
        state:int|TicketState=TicketState.CREATED
    ):
        category_value = category if isinstance(category, int) else TicketCategory.UNDEFINED.value
        state_value = state if isinstance(state, int) else TicketState.CREATED.value
        ticket_dto = TicketDTO(ticket_id, description, category_value, state_value)
        errors = EnsureTicket.partialValidate(ticket_dto._asdict())
        if len(errors) > 0:
            raise PresentationError("\n".join(errors))
        return ticket_dto
