from collections import namedtuple
from enum import Enum

from validator_collection import checkers

from .DomainError import DomainError
from .utils.identity import Identity, IdentityAlgorithm


class TicketCategory(Enum):
    UNDEFINED = "U"
    HOTFIX = "H"
    BUGFIX = "B"
    FEATURE = "F"
    REFACTOR = "R"
    DOCS = "D"


class TicketState(Enum):
    UNDIFINED = "U"
    CREATED = "C"
    IN_PROCESS = "P"
    OBSERVE = "O"
    END = "E"


TicketStruct = namedtuple("ticket", ["ticket_id", "description", "category", "state"])


class Ticket:
    @classmethod
    def validate(cls, my_ticket: dict) -> TicketStruct:
        print("---VALIDATE---")
        print(my_ticket)
        errors = list()

        ticket_id_error = cls.validateTicketId(my_ticket.get("ticket_id"))
        if len(ticket_id_error) > 0:
            errors.append(ticket_id_error)

        description_error = cls.validateDescription(my_ticket.get("description"))
        if len(description_error) > 0:
            errors.append(description_error)

        category_error = cls.validateCategory(my_ticket.get("category"))
        if len(category_error) > 0:
            errors.append(category_error)

        state_error = cls.validateState(my_ticket.get("state"))
        if len(state_error) > 0:
            errors.append(state_error)

        if len(errors) > 0:
            raise DomainError(errors)

        return TicketStruct(**my_ticket)

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

    @staticmethod
    def validateState(state: str) -> str:
        for member in TicketState:
            if member.value == state:
                return ""
        return "Invalid state"

    @staticmethod
    def validateCategory(category: str) -> str:
        for member in TicketCategory:
            if member.value == category:
                return ""
        return "Invalid state"

    @classmethod
    def fromDict(cls, params: dict):
        my_ticket = {k: v for k, v in params.items() if k in TicketStruct._fields}

        return cls.create(**my_ticket)

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
