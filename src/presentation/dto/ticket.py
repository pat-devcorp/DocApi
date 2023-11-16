from collections import namedtuple

from ...domain.dao.ticket import TicketCategory, TicketDAO, TicketState, ValidTicket
from ..PresentationError import PresentationError

TicketDTO = namedtuple("TicketDTO", ["description", "category", "state"])


class TicketHandler:
    @staticmethod
    def getMock() -> TicketDTO:
        return TicketDTO(
            description="Test task",
            category=TicketCategory.UNDEFINED,
            state=TicketState.CREATED,
        )

    @staticmethod
    def getIdentifier(ticket_id):
        return TicketDAO.getIdentifier(ticket_id)

    @staticmethod
    def fromDict(params: dict) -> TicketDTO | PresentationError:
        data = {k: params.get(k, None) for k in TicketDTO._fields}
        is_ok, err = ValidTicket.isValid(data)
        if not is_ok:
            raise PresentationError("\n".join(err))

        if (category := data.get("category")) is not None:
            data["category"] = TicketCategory(category)

        if (state := data.get("state")) is not None:
            data["state"] = TicketCategory(state)

        return TicketDTO(**data)

    @staticmethod
    def create(
        description: str,
        category: int = TicketCategory.UNDEFINED.value,
        state: int = TicketState.CREATED.value,
    ) -> TicketDTO | PresentationError:
        data = {"description": description, "category": category, "state": state}
        is_ok, err = ValidTicket.isValid(data, False)
        if not is_ok:
            raise PresentationError("\n".join(err))

        ticket_category = TicketCategory(category)
        ticket_state = TicketState(state)
        return TicketDTO(description, ticket_category, ticket_state)
