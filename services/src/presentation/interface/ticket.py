from collections import namedtuple

from validator_collection import checkers

from .InterfaceError import InterfaceError
from ...utils.identity import Identity, IdentityAlgorithm
from ...domain.ticket import TicketState, TicketCategory, validateState, validateCategory


TicketStruct = namedtuple("ticket", ["ticket_id", "description", "category", "state"])


class Ticket:
    @classmethod
    def validate(cls, ticket_dto: dict) -> TicketStruct:
        print("---VALIDATE---")
        print(ticket_dto)
        errors = list()

        ticket_id_error = cls.validateTicketId(ticket_dto.get("ticket_id"))
        if len(ticket_id_error) > 0:
            errors.append(ticket_id_error)

        description_error = cls.validateDescription(ticket_dto.get("description"))
        if len(description_error) > 0:
            errors.append(description_error)

        category_error = validateCategory(ticket_dto.get("category"))
        if len(category_error) > 0:
            errors.append(category_error)

        state_error = validateState(ticket_dto.get("state"))
        if len(state_error) > 0:
            errors.append(state_error)

        if len(errors) > 0:
            raise InterfaceError(errors)

        return TicketStruct(**ticket_dto)

    @staticmethod
    def validateTicketId(ticket_id: str) -> str:
        if not Identity.validate(ticket_id, IdentityAlgorithm.UUID_V4):
            return "Identity not valid for ticket"
        return ""

    @staticmethod
    def validateDescription(description: str) -> str:
        if description is None or len(description) == 0:
            return "Empty description"

        if not checkers.is_string(description, maximum_lengt=200):
            return "Max length exceeded, not allowed"
        return ""

    @classmethod
    def fromDict(cls, params: dict):
        ticket_dto = {k: v for k, v in params.items() if k in TicketStruct._fields}

        return cls.create(**ticket_dto)

    @classmethod
    def create(
        cls,
        ticket_id: Identity,
        description: str,
        category: TicketCategory = TicketCategory.UNDEFINED,
        state: TicketState = TicketState.UNDIFINED,
    ) -> TicketStruct:
        return cls.validate(
            {
                "ticket_id": str(ticket_id),
                "description": description,
                "category": category.value,
                "state": state.value,
            }
        )
