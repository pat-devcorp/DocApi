from collections import namedtuple
from enum import Enum

from ...domain.DomainError import DomainError
from ...utils.DatetimeHandler import DateTimeHandler, check_datetime_format
from ...utils.ResponseHandler import ID_NOT_VALID, SCHEMA_NOT_MATCH
from ..IdentifierHandler import IdentifierHandler, IdentityAlgorithm

TicketIdentifier = namedtuple("TicketIdentifier", "value")
Ticket = namedtuple(
    "Ticket",
    [
        "ticketId",
        "description",
        "category",
        "typeCommit",
        "state",
        "points",
        "estimateEndAt",
    ],
)
PartialTicket = namedtuple(
    "PartialTicket", Ticket._fields, defaults=[None] * (len(Ticket._fields) - 1)
)


class TicketCategory(Enum):
    UNDEFINED = 0
    PENDENTS = 1
    SUPPORT = 2
    TICKET = 3


class TicketTypeCommit(Enum):
    UNDEFINED = 0
    FEAT = 1
    FIX = 2
    BUILD = 3
    CI = 4
    DOCS = 5
    CHORE = 6
    PERFORMANCE = 6
    REFACTOR = 7
    LINTER = 8
    TEST = 9


class TicketState(Enum):
    CREATED = 0
    DELETED = 1
    IN_PROCESS = 2
    OBSERVE = 3
    END = 4


class TicketValidator:
    @staticmethod
    def is_valid_identifier(identifier: str):
        try:
            TicketDomain.set_identifier(identifier)
            return True, ""
        except DomainError:
            return False, "Invalid identifier"

    @staticmethod
    def is_valid_state(state: int) -> tuple[bool, str]:
        for member in TicketState:
            if member.value == state:
                return True, ""
        return False, "Invalid state"

    @staticmethod
    def is_valid_points(points: int):
        if points > 0 and points < 11:
            return False, "Invalid points, be more than 0 and less than ten"
        return True, ""

    @staticmethod
    def is_valid_category(category: int) -> tuple[bool, str]:
        for member in TicketCategory:
            if member.value == category:
                return True, ""
        return False, "Invalid category"

    @staticmethod
    def is_valid_typeCommit(typeCommit: int) -> tuple[bool, str]:
        for member in TicketTypeCommit:
            if member.value == typeCommit:
                return True, ""
        return False, "Invalid commit type"

    @staticmethod
    def is_valid_endAt(estimateEndAt: str) -> tuple[bool, str]:
        if not check_datetime_format(estimateEndAt):
            return False, "Date of end format not valid"
        return True, ""


class TicketSanitizer:
    @staticmethod
    def sanitary_description(description: str) -> str:
        try:
            return description.decode("utf8")
        except UnicodeDecodeError as u:
            raise DomainError(u)


class TicketDomain:
    _idAlgorithm = IdentityAlgorithm.UUID_V4

    @classmethod
    def get_identifier(cls) -> TicketIdentifier:
        ic = IdentifierHandler.get_default(cls._idAlgorithm)
        return TicketIdentifier(ic)

    @classmethod
    def set_identifier(cls, identifier) -> TicketIdentifier | DomainError:
        is_ok, err = IdentifierHandler.is_valid(identifier, cls._idAlgorithm)
        if not is_ok:
            raise DomainError(ID_NOT_VALID, err)
        return TicketIdentifier(identifier)

    @staticmethod
    def is_valid(ref_object: dict, is_partial=True) -> tuple[bool, str]:
        validate_func = {
            "ticketId": TicketValidator.is_valid_identifier,
            "category": TicketValidator.is_valid_category,
            "typeCommit": TicketValidator.is_valid_typeCommit,
            "state": TicketValidator.is_valid_state,
            "points": TicketValidator.is_valid_points,
            "estimateEndAt": TicketValidator.is_valid_endAt,
        }

        errors = list()
        for k, v in ref_object.items():
            if is_partial and v is None:
                continue
            if (func := validate_func.get(k)) is not None:
                is_ok, err = func(v)
                if not is_ok:
                    errors.append(err)

        if len(errors) > 0:
            return False, "\n".join(errors)

        return True, ""

    @staticmethod
    def sanitize(data: dict) -> dict:
        sanitize_data = data

        if (description := sanitize_data.get("description")) is not None:
            sanitize_data["description"] = TicketSanitizer.sanitary_description(description)

        return sanitize_data

    @classmethod
    def from_dict(cls, data: dict) -> Ticket | DomainError:
        item = {k: v for k, v in data.items() if k in Ticket._fields}
        ok, err = TicketValidator.is_valid(item, False)
        if not ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)

        sanitize_item =  cls.sanitize(item)

        return Ticket(
            sanitize_item["ticketId"],
            sanitize_item["description"],
            sanitize_item["category"],
            sanitize_item["typeCommit"],
            sanitize_item["state"],
            sanitize_item["points"],
            sanitize_item["estimateEndAt"],
        )

    @classmethod
    def partial_ticket(
        cls, identifier: TicketIdentifier, data: dict
    ) -> dict | DomainError:
        item = {k: v for k, v in data.items() if k in Ticket._fields}
        ok, err = TicketValidator.is_valid(item)
        if not ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)
        
        return PartialTicket(identifier.value, **item)

    @classmethod
    def new_ticket(
        cls, identifier: TicketIdentifier, description: str
    ) -> Ticket | DomainError:
        is_ok, err = TicketValidator.is_valid_description(description)
        if not is_ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)
        
        sanitize_description =  TicketSanitizer.sanitary_description(description)

        return Ticket(
            identifier.value,
            sanitize_description,
            TicketCategory.PENDENTS.value,
            TicketTypeCommit.UNDEFINED.value,
            TicketState.CREATED.value,
            1,
            DateTimeHandler.now().value,
        )

    @staticmethod
    def bad_ticket() -> Ticket:
        return Ticket(
            "a",
            "a" * 201,
            100,
            100,
            100,
            100,
            "20/20/20",
        )
