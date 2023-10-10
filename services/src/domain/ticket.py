from collections import namedtuple
from enum import Enum

from ..utils.IdentityHandler import IdentityAlgorithm, IdentityHandler


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
