from collections import namedtuple
from enum import Enum

from validator_collection import checkers

from ..utils.IdentityHandler import IdentityAlgorithm, IdentityHandler


class TicketCategory(Enum):
    UNDEFINED = 0
    HOTFIX = 1
    BUGFIX = 2
    FEATURE = 3
    REFACTOR = 4
    DOCS = 5


class TicketState(Enum):
    UNDIFINED = 0
    DELETED = 1
    CREATED = 2
    IN_PROCESS = 3
    OBSERVE = 4
    END = 5


TicketStruct = namedtuple("ticket", ["ticket_id", "description", "category", "state"])


class Ticket:
    @classmethod
    def partialValidate(cls, ref_ticket: dict) -> str:
        print("---DOMAIN---")
        print(ref_ticket)
        validate_funcs = {
            "ticket_id": cls.validateTicketId,
            "description": cls.validateDescription,
            "category": cls.validateCategory,
            "state": cls.validateState,
        }

        ticket = {k: v for k, v in ref_ticket.items() if k in validate_funcs.keys()}

        errors = list()
        for k, v in ticket.items():
            func = validate_funcs[k]
            err = func(v)
            if len(err) > 0:
                errors.append(err)

        if len(errors) > 0:
            return "\n".join(errors)

        return None

    @staticmethod
    def validateTicketId(ticket_id: str) -> str:
        if not IdentityHandler.validate(ticket_id, IdentityAlgorithm.UUID_V4):
            return "Identity not valid for ticket"
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

    @staticmethod
    def validateDescription(description: str) -> str:
        if not checkers.is_string(description, maximum_lengt=200):
            return "Max length exceeded, not allowed"
        return ""
