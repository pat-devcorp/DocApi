from collections import namedtuple

from ...utils.response_code import FIELD_REQUIRED, ID_NOT_FOUND
from ..DomainError import DomainError
from ..enum.ticket_status import TicketState
from ..identifier_handler import Identifier, IdentifierAlgorithm, IdentifierHandler
from ..str_funcs import StrValidator

TicketId = namedtuple("TicketId", ["value"])
Ticket = namedtuple(
    "Ticket",
    [
        "ticketId",
        "channelId",
        "requirement",
        "because",
        "state",
    ],
)


class TicketDomain:
    _idAlgorithm = IdentifierAlgorithm.UUID_V4
    pk = "ticketId"

    @classmethod
    def get_default_identifier(cls):
        return TicketId(IdentifierHandler.get_default_identifier(cls.algorithm))

    @classmethod
    def set_identifier(cls, identifier):
        IdentifierHandler.is_valid(cls.algorithm, identifier)
        return TicketId(identifier)

    @staticmethod
    def as_dict(namedtuple_instance) -> dict:
        return dict(namedtuple_instance._asdict())

    @classmethod
    def from_dict(cls, data: list) -> Ticket | DomainError:
        if data.get(cls.pk) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        ticket = {k: v for k, v in data.items() if k in Ticket._fields}
        cls.is_valid(ticket)
        return Ticket(**ticket)

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
        ticketId: TicketId,
        channelId: Identifier,
        requirement: str,
        because: str,
    ) -> Ticket | DomainError:
        if (
            ticketId is None
            or channelId is None
            or StrValidator.is_empty_string(requirement)
            or StrValidator.is_empty_string(because)
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")

        item = {
            "ticketId": ticketId.value,
            "channelId": channelId.value,
            "requirement": requirement,
            "because": because,
            "state": TicketState.CREATED.value,
        }

        return cls.from_dict(item)
