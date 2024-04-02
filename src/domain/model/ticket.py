from collections import namedtuple

from ...utils.status_code import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT
from ..custom_string import CustomString
from ..DomainError import DomainError
from ..enum.ticket_status import TicketState
from ..identifier_handler import IdentifierAlgorithm, IdentifierHandler

Ticket = namedtuple(
    "Ticket",
    [
        "ticket_id",
        "channel_id",
        "requirement",
        "because",
        "state",
    ],
)


class TicketDomain:
    _idAlgorithm = IdentifierAlgorithm.UUID_V4
    pk = "ticket_id"

    @classmethod
    def get_default_identifier(cls):
        return IdentifierHandler.get_default_identifier(cls.algorithm)

    @classmethod
    def set_identifier(cls, identifier):
        return IdentifierHandler.is_valid(cls.algorithm, identifier)

    @staticmethod
    def as_dict(namedtuple_instance) -> dict:
        return dict(namedtuple_instance._asdict())

    @classmethod
    def from_dict(cls, data: list) -> Ticket | DomainError:
        if data.get(cls.pk) is None:
            raise DomainError(ID_NOT_FOUND, "id must be provided")

        item = dict()
        for k in Ticket._fields:
            item[k] = data.get(k, None)

        return cls.is_valid(item)

    @classmethod
    def is_valid(
        cls,
        ticket_id,
        channel_id,
        requirement,
        because,
        state,
    ) -> Ticket | DomainError:
        errors = list()

        if ticket_id is not None:
            try:
                cls.set_identifier(ticket_id)
            except DomainError as e:
                errors.append(str(e))

        if state is not None:
            is_ok, err = TicketState.has_value(state)
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

        return Ticket(
            ticket_id,
            channel_id,
            requirement,
            because,
            state,
        )

    @classmethod
    def new(
        cls,
        ticket_id: IdentifierHandler,
        channel_id: IdentifierHandler,
        requirement: str,
        because: str,
        state: TicketState = None,
    ) -> Ticket | DomainError:
        if (
            ticket_id is None
            or channel_id is None
            or CustomString.is_empty_string(requirement)
            or CustomString.is_empty_string(because)
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        state = TicketState.CREATED.value if state is None else state.value

        return cls.is_valid(
            ticket_id,
            channel_id,
            requirement,
            because,
            state,
        )
