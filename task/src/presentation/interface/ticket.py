from collections import namedtuple

from ...domain.ticket import Ticket as TicketDomain
from .InterfaceError import InterfaceError

TicketDTO = namedtuple(
    "TicketDTO", ["write_uid", "ticket_id", "description", "category", "state"]
)


class Ticket:
    def _validate(ticket_dto: dict) -> list:
        print("---INTERFACE---")
        print(ticket_dto)

        errors = list()

        domain_error = TicketDomain.partialValidate(ticket_dto)
        if domain_error is not None:
            errors.append(domain_error)

        return errors

    def _validateRequiredParams(params: dict):
        if params.get("write_uid") is None:
            raise InterfaceError("User must be provided")

        if params.get("ticket_id") is None:
            raise InterfaceError("Identifier must be provided")

    @classmethod
    def getDefault(cls):
        return {
            "write_uid": None,
            "ticket_id": None,
            "description": "",
            "category": 0,
            "state": 0,
        }

    @classmethod
    def fromDict(cls, params: dict):
        cls._validateRequiredParams(params)

        ticket_dto = dict()
        for k in TicketDTO._fields:
            ticket_dto[k] = params[k] if params.get(k) is not None else None

        errors = cls._validate(params)
        if len(errors) > 0:
            raise InterfaceError("\n".join(errors))

        return TicketDTO(**ticket_dto)
