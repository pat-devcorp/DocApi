from collections import namedtuple

from ...domain.ticket import Ticket as TicketDomain
from .InterfaceError import InterfaceError

TicketDTO = namedtuple(
    "TicketDTO", ["write_uid", "ticket_id", "description", "category", "state"]
)


AccessTicketDTO = namedtuple("AccessTicketDTO", ["write_uid", "ticket_id"])


class Ticket:
    @classmethod
    def validate(cls, ticket_dto: dict) -> TicketDTO:
        print("---INTERFACE---")
        print(ticket_dto)

        errors = list()

        description_error = TicketDomain.validateDescription(ticket_dto.get("description"))
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

    @classmethod
    def fromDict(cls, params: dict):
        ticket_dto = {k: v for k, v in params.items() if k in TicketDTO._fields}
        return cls.create(**ticket_dto)

    @classmethod
    def create(
        cls,
        write_uid: str,
        ticket_id: str,
        description: str,
        category: int = 0,
        state: int = 0,
    ):
        return cls.validate(
            {
                "write_uid": write_uid,
                "ticket_id": ticket_id,
                "description": description,
                "category": category,
                "state": state,
            }
        )

    @classmethod
    def createAcessDTO(cls, params: dict):
        errors = list()

        ticket_id_error = TicketDomain.validateTicketId(params.get("ticket_id"))
        if len(ticket_id_error) > 0:
            errors.append(ticket_id_error)

        if params.get("write_uid") is None:
            errors.append("User must be provided")

        if len(errors) > 0:
            raise InterfaceError(errors)

        return AccessTicketDTO(params["write_uid"], params["ticket_id"])
