from collections import namedtuple

from ...utils.status_code import FIELD_REQUIRED, ID_NOT_FOUND, INVALID_FORMAT
from ..custom_dict import CustomDict
from ..custom_string import CustomString
from ..DomainError import DomainError
from ..enum.channel_type import ChannelType
from ..enum.commit_type import CommitType
from ..enum.identifier_algorithm import IdentifierAlgorithm
from ..enum.ticket_state import TicketState
from ..identifier_handler import IdentifierHandler

Ticket = namedtuple(
    "Ticket",
    [
        "ticket_id",
        "channel_type",
        "requirement",
        "because",
        "state",
        "attrs",
    ],
)


class TicketDomain:
    algorithm = IdentifierAlgorithm.SONY_FLAKE
    pk = "ticket_id"

    @staticmethod
    def get_invalid_ticket():
        return Ticket(
            ticket_id=0,
            channel_type="A",
            requirement="asdasdasd",
            because="asdasdas",
            state="A",
            attrs=list(),
        )

    @classmethod
    def get_valid_ticket(cls):
        identifier = cls.get_default_identifier()
        return Ticket(
            ticket_id=identifier.value,
            channel_type=ChannelType.MAIL.value,
            requirement="test",
            because="help with development",
            state=TicketState.CREATED.value,
            attrs={"type_commit": CommitType.FIX.value},
        )

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
        channel_type,
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

        if channel_type is not None:
            is_ok, err = ChannelType.has_value(channel_type)
            if not is_ok:
                errors.append(err)

        if attrs is not None:
            if not CustomDict.has_only_primitive_types(attrs):
                errors.append("the dictionary must have only primitive types")

        if len(errors) > 0:
            raise DomainError(INVALID_FORMAT, "\n".join(errors))

    @classmethod
    def new(
        cls,
        ticket_id: IdentifierHandler,
        channel_type: ChannelType | int,
        requirement: str,
        because: str,
        state: TicketState | int,
        attrs: dict = None,
    ) -> Ticket | DomainError:
        if (
            not isinstance(ticket_id, IdentifierHandler)
            or not isinstance(channel_type, (ChannelType, int))
            or not isinstance(state, (TicketState, int))
        ):
            raise DomainError(FIELD_REQUIRED, "fields must be provided")
        channel_type_value = (
            channel_type.value
            if isinstance(channel_type, ChannelType)
            else channel_type
        )
        state_value = state.value if isinstance(state, TicketState) else state
        if attrs is None:
            attrs = dict()

        cls.is_valid(
            ticket_id.value,
            channel_type_value,
            requirement,
            because,
            state_value,
            attrs,
        )

        return Ticket(
            ticket_id.value,
            channel_type_value,
            requirement,
            because,
            state_value,
            attrs,
        )
