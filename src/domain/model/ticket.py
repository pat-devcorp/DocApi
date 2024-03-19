from collections import namedtuple

from ...utils.response_code import ID_NOT_VALID, SCHEMA_NOT_MATCH
from ..DomainError import DomainError
from ..enum.ticket_status import TicketState
from ..identifier_handler import Identifier, IdentifierHandler, IdentityAlgorithm

Ticket = namedtuple(
    "Ticket",
    [
        "ticketId",
        "where",
        "requirement",
        "because",
        "state",
    ],
)
PartialTicket = namedtuple(
    "PartialTicket", Ticket._fields, defaults=[None] * (len(Ticket._fields) - 1)
)


class TicketDomain:
    _idAlgorithm = IdentityAlgorithm.UUID_V4
    _pk = "ticketId"

    @classmethod
    def get_identifier(cls) -> Identifier:
        identifier = IdentifierHandler.get_default(cls._idAlgorithm)
        return Identifier(identifier, cls._idAlgorithm, cls._pk)

    @classmethod
    def is_valid_identifier(cls, identifier) -> None | DomainError:
        is_ok, err = IdentifierHandler.is_valid(identifier, cls._idAlgorithm)
        if not is_ok:
            raise DomainError(ID_NOT_VALID, err)

    @classmethod
    def set_identifier(cls, identifier) -> Identifier | DomainError:
        cls.is_valid_identifier(identifier)
        return Identifier(identifier, cls._idAlgorithm, cls._pk)

    @staticmethod
    def as_dict(ticket: Ticket | PartialTicket) -> dict:
        return {k: v for k, v in ticket._asdict().items() if k is not None}

    @classmethod
    def from_dict(
        cls, identifier: Identifier, data: list
    ) -> Ticket | PartialTicket | DomainError:
        item = {k: v for k, v in data.items() if k in Ticket._fields}
        item[cls._pk] = identifier.value

        is_ok, err = cls.is_valid(item)
        if not is_ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)

        if Ticket._fields != set(item.keys()):
            return PartialTicket(**item)
        return Ticket(**item)

    @classmethod
    def from_repo(cls, data: list) -> Ticket | PartialTicket:
        item = {k: v for k, v in data.items() if k in Ticket._fields}

        if Ticket._fields != set(item.keys()):
            return PartialTicket(**item)
        return Ticket(**item)

    @classmethod
    def is_valid(cls, data: dict, is_partial=True) -> tuple[bool, str]:
        validate_func = {
            "ticketId": [cls.is_valid_identifier],
            "state": [TicketState.has_value],
        }

        errors = list()
        for k, v in data.items():
            if is_partial and v is None:
                continue
            if (functions := validate_func.get(k)) is not None:
                for function in functions:
                    is_ok, err = function(v)
                    if not is_ok:
                        errors.append(err)

        if len(errors) > 0:
            return False, "\n".join(errors)
        return True, ""

    @classmethod
    def new(
        cls,
        identifier: Identifier,
        where,
        requirement: str,
        because: str,
    ) -> Ticket | DomainError:
        item = {
            "ticketId": identifier.value,
            "where": where.value,
            "requirement": requirement,
            "because": because,
            "state": TicketState.CREATED.value,
        }

        return Ticket(**item)

    # Test
    @staticmethod
    def bad_ticket():
        return Ticket(
            "a",
            "a" * 201,
            100,
            100,
            100,
            100,
            "20/20/20",
        )
