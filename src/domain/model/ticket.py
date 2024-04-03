from collections import namedtuple

from ...utils.status_code import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT
from ..custom_string import CustomString
from ..DomainError import DomainError
from ..enum.identifier_algorithm import IdentifierAlgorithm
from ..enum.ticket_status import TicketState
from ..enum.type_channel import TypeChannel
from ..identifier_handler import IdentifierHandler

Ticket = namedtuple(
    "Ticket",
    [
        "ticket_id",
        "type_channel",
        "requirement",
        "because",
        "state",
        "attrs",
    ],
)


class TicketDomain:
    algorithm = IdentifierAlgorithm.SONY_FLAKE
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

        item = {k: data.get(k, None) for k in Ticket._fields}
        attrs = {k: v for k, v in data.items() if k not in Ticket._fields}
        item["attrs"] = attrs

        cls.is_valid(**item)
        return Ticket(**item)

    @classmethod
    def is_valid(
        cls,
        ticket_id,
        type_channel,
        requirement,
        because,
        state,
        attrs,
    ) -> Ticket | DomainError:
        errors = list()

        if ticket_id is not None:
            try:
                cls.set_identifier(ticket_id)
            except DomainError as e:
                errors.append(str(e))

        if requirement is not None:
            if CustomString.is_empty_string(requirement):
                errors.append("invalid requirement")

        if because is not None:
            if CustomString.is_empty_string(because):
                errors.append("invalid because")

        if state is not None:
            is_ok, err = TicketState.has_value(state)
            if not is_ok:
                errors.append(err)

        if type_channel is not None:
            is_ok, err = TypeChannel.has_value(type_channel)
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

    @classmethod
    def new(
        cls,
        ticket_id: IdentifierHandler,
        type_channel: TypeChannel,
        requirement: str,
        because: str,
        state: TicketState = None,
        attrs: dict = None,
    ) -> Ticket | DomainError:
        if not isinstance(ticket_id, IdentifierHandler) or not isinstance(
            type_channel, TypeChannel
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        type_channel_value = type_channel.value
        state_value = (
            TicketState.CREATED.value
            if not isinstance(state, TicketState)
            else state.value
        )
        if attrs is None:
            attrs = dict()

        cls.is_valid(
            ticket_id.value,
            type_channel_value,
            requirement,
            because,
            state_value,
            attrs,
        )

        return Ticket(
            ticket_id.value,
            type_channel_value,
            requirement,
            because,
            state_value,
            attrs,
        )
