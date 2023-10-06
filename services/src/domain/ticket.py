from enum import Enum

from ..presentation.interface.ticket import TicketStruct


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

class Ticket:
    def __init__(self, my_ticket_struct: TicketStruct):
        print(my_ticket_struct)
    
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