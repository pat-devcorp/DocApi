from collections import namedtuple
from enum import Enum

from validator_collection import checkers

from .DomainError import DomainError
from .utils.identity import Identity, IdentityAlgorithm


class TypeTicket(Enum):
    UNDEFINED = 0
    HOTFIX = 1
    BUGFIX = 2
    FEATURE = 3
    REFACTOR = 4
    DOCS = 5


class StateTicket(Enum):
    UNDIFINED = "U"
    CREATED = "C"
    IN_PROCESS = "P"
    OBSERVE = "O"
    END = "E"


TicketStruct = namedtuple(
    "ticket", ["ticket_id", "type_ticket", "description", "state"]
)


class Ticket:
    @staticmethod
    def validate(my_ticket: dict) -> TicketStruct:
        errors = list()

        my_ticket_id = my_ticket.get("ticket_id")
        ticket_id_error = Ticket.ensureTicketId(my_ticket_id)
        if len(ticket_id_error) > 0:
            errors.append(ticket_id_error)

        description_error = Ticket.ensureDescription(my_ticket.get("description"))
        if len(description_error) > 0:
            errors.append(description_error)

        my_type_ticket = my_ticket.get("ticket_type")
        type_ticket_error = Ticket.ensureType(my_type_ticket)
        if len(type_ticket_error) > 0:
            errors.append(type_ticket_error)

        my_state = my_ticket.get("state")
        state_error = Ticket.ensureState(my_state)
        if len(state_error) > 0:
            errors.append(state_error)

        if len(errors) > 0:
            raise DomainError(errors)

        return TicketStruct(**my_ticket)

    @staticmethod
    def ensureTicketId(ticket_id: str) -> str:
        if not Identity.validate(ticket_id, IdentityAlgorithm(1)):
            return "Identity not valid for ticket"
        return ""

    @staticmethod
    def ensureDescription(description: str) -> str:
        if description is None or len(description) == 0:
            return "Empty description"

        if checkers.is_string(description, maximum_lengt=200):
            return "Max length exceeded, not allowed"
        return ""

    @staticmethod
    def ensureState(state_ticket: str) -> str:
        if state_ticket not in StateTicket:
            return "Invalid state"
        return ""

    @staticmethod
    def ensureTicketId(ticket_id: str) -> str:
        if not Identity.validate(ticket_id, IdentityAlgorithm(1)):
            return "Identity not valid for ticket"
        return ""

    @classmethod
    def fromDict(cls, params):
        my_ticket = {k: v for k, v in params.items() if k in TicketStruct._fields}

        cls.create(**my_ticket)

    @classmethod
    def create(
        self,
        ticket_id: Identity(IdentityAlgorithm(1)),
        description: str,
        type_ticket: TypeTicket = TypeTicket.UNDEFINED,
        state: StateTicket = StateTicket.UNDIFINED,
    ) -> TicketStruct:
        my_ticket = {
            "ticket_id": ticket_id,
            "description": description,
            "type_ticket": type_ticket,
            "state": state,
        }
        return self.validate(my_ticket)
