from collections import namedtuple

from ...domain.dao.ticket import (
    TicketCategory,
    TicketDAO,
    TicketState,
    TicketTypeCommit,
    ValidTicket,
)
from ...utils.ErrorHandler import PRESENTATION_VALIDATION
from ..PresentationError import PresentationError

TicketDTO = namedtuple("TicketDTO", ["description", "category", "type_commit", "state"])


class TicketHandler:
    @staticmethod
    def getMock() -> TicketDTO:
        return TicketDTO(
            description="Test task",
            category=TicketCategory.UNDEFINED,
            type_commit=TicketTypeCommit.UNDEFINED,
            state=TicketState.CREATED,
        )
    
    @classmethod
    def serialize(cls, data: dict):
        return {k: v for k, v in data.items() if k in TicketDTO._fields}

    @staticmethod
    def getIdentifier(ticket_id):
        return TicketDAO.getIdentifier(ticket_id)

    @staticmethod
    def fromDict(params: dict) -> TicketDTO | PresentationError:
        data = {k: params.get(k, None) for k in TicketDTO._fields}
        is_ok, err = ValidTicket.isValid(data)
        if not is_ok:
            raise PresentationError(PRESENTATION_VALIDATION, "\n".join(err))

        if (category := data.get("category")) is not None:
            data["category"] = TicketCategory(category)

        if (type_commit := data.get("type_commit")) is not None:
            data["type_commit"] = TicketTypeCommit(type_commit)

        if (state := data.get("state")) is not None:
            data["state"] = TicketCategory(state)

        return TicketDTO(**data)

    @staticmethod
    def create(
        description: str,
        category: int = TicketCategory.UNDEFINED.value,
        type_commit: int = TicketTypeCommit.UNDEFINED.value,
        state: int = TicketState.CREATED.value,
    ) -> TicketDTO | PresentationError:
        data = {
            "description": description,
            "category": category,
            "type_commit": type_commit,
            "state": state,
        }
        is_ok, err = ValidTicket.isValid(data, False)
        if not is_ok:
            raise PresentationError(PRESENTATION_VALIDATION, "\n".join(err))

        ticket_category = TicketCategory(category)
        ticket_type_commit = TicketTypeCommit(type_commit)
        ticket_state = TicketState(state)
        return TicketDTO(description, ticket_category, ticket_type_commit, ticket_state)
