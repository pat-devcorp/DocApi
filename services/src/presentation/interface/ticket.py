from collections import namedtuple

from validator_collection import checkers

from ...domain.ticket import Ticket as TicketDomain
from ...utils.AuditHandler import AuditStruct
from .InterfaceError import InterfaceError

TicketDTO = namedtuple(
    "ticket",
    ["ticket_id", "description", "category", "state"] + list(AuditStruct._fields),
)


class Ticket:
    @classmethod
    def validate(cls, ticket_dto: dict) -> TicketDTO:
        print("---INTERFACE---")
        print(ticket_dto)

        errors = list()

        description_error = cls.validateDescription(ticket_dto.get("description"))
        if len(description_error) > 0:
            errors.append(description_error)

        ticket_id_error = TicketDomain.validateTicketId(ticket_dto.get("ticket_id"))
        if len(ticket_id_error) > 0:
            errors.append(ticket_id_error)

        category_error = TicketDomain.validateCategory(ticket_dto.get("category"))
        if len(category_error) > 0:
            errors.append(category_error)

        state_error = TicketDomain.validateState(ticket_dto.get("state"))
        if len(state_error) > 0:
            errors.append(state_error)

        if len(errors) > 0:
            raise InterfaceError(errors)

        return TicketDTO(**ticket_dto)

    @staticmethod
    def validateIdentity(ticket_id: str) -> str:
        if ticket_id is None or len(ticket_id) == 0:
            return "Empty identity"

        ticket_id_error = TicketDomain.validateTicketId(ticket_id)
        if len(ticket_id_error) > 0:
            return ticket_id_error
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
        ticket_dto = {k: v for k, v in params.items() if k in TicketDTO._fields}
        return cls.create(**ticket_dto)

    @classmethod
    def create(
        cls,
        ticket_id: str,
        description: str,
        category: str = "U",
        state: str = "U",
    ):
        return cls.validate(
            {
                "ticket_id": ticket_id,
                "description": description,
                "category": category,
                "state": state,
            }
        )
