from collections import namedtuple

from ..DomainError import DomainError
from ..custon_enum import CustomEnum
from ...utils.custom_date import CustomDate
from ...utils.response_code import ID_NOT_VALID, SCHEMA_NOT_MATCH
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


class TicketCategory(CustomEnum):
    UNDEFINED = 0
    PENDENTS = 1
    SUPPORT = 2
    TICKET = 3


class TicketTypeCommit(CustomEnum):
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


class TicketState(CustomEnum):
    CREATED = 0
    DELETED = 1
    IN_PROCESS = 2
    OBSERVE = 3
    END = 4


class TicketDomain:
    _idAlgorithm = IdentityAlgorithm.UUID_V4

    @classmethod
    def get_identifier(cls) -> TicketIdentifier:
        ic = IdentifierHandler.get_default(cls._idAlgorithm)
        return TicketIdentifier(ic)


    @classmethod
    def is_valid_identifier(cls) -> None | DomainError:
        is_ok, err = IdentifierHandler.is_valid(identifier, cls._idAlgorithm)
        if not is_ok:
            raise DomainError(ID_NOT_VALID, err)


    @classmethod
    def set_identifier(cls, identifier) -> TicketIdentifier | DomainError:
        cls.is_valid_identifier(identifier)
        return TicketIdentifier(identifier)


    @staticmethod
    def is_valid_points(value: int) -> tuple[bool, str]:
        if (0 <= value <= 10):
            return True, ""
        return False, "Points must be between 0 and 10"


    @staticmethod
    def to_utf8(value: str) -> str:
        try:
            return value.decode("utf8")
        except UnicodeDecodeError as u:
            raise ValueError(u)


    @classmethod
    def is_valid(cls, data: dict, is_partial=True) -> tuple[bool, str]:
        validate_func = {
            "ticketId": [TicketValidator.is_valid_identifier],
            "category": [TicketCategory.has_value],
            "typeCommit": [TicketTypeCommit.has_value],
            "state": [TicketState.has_value],
            "points": [cls.is_valid_points],
            "estimateEndAt": [CustomDatetime.check_format],
        }

        errors = list()
        for k, v in data.items():
            if is_partial and v is None:
                continue
            if (funcs := validate_func.get(k)) is not None:
                for func in funcs:
                    is_ok, err = func(v)
                    if not is_ok:
                        errors.append(err)

        if len(errors) > 0:
            return False, "\n".join(errors)
        return True, ""


    @staticmethod
    def sanitize(data: dict) -> dict:
        sanitize_data = dict(data)
        if (description := sanitize_data.get("description")) is not None:
            sanitize_data["description"] = TicketSanitizer.sanitary_description(description)

        return sanitize_data


    @classmethod
    def from_dict(cls, data: list) -> Ticket | PartialTicket | DomainError:
        item = {k: v for k, v in data.items() if k in Ticket._fields}

        is_ok, err = cls.is_valid(item)
        if not is_ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)
        sanitize_item = cls.sanitize(item)

        if Ticket._fields == set(item.keys()):
            return Ticket(**sanitize_item)
        return PartialTicket(**sanitize_item)
    
    @classmethod
    def from_repo(cls, data: list) -> Ticket | PartialTicket:
        item = {k: v for k, v in data.items() if k in Ticket._fields}

        if Ticket._fields == set(item.keys()):
            return Ticket(**item)
        return PartialTicket(**item)
    

    @classmethod
    def new_ticket(
        cls, identifier: TicketIdentifier, description: str
    ) -> Ticket | DomainError:
        item = {
            "ticketId": identifier.value,
            "description": to_utf8(description),
            "category": TicketCategory.PENDENTS.value,
            "typeCommit": TicketTypeCommit.UNDEFINED.value,
            "state": TicketState.CREATED.value,
            "points": 1,
            "estimateEndAt": CustomDate.now().value,
        }

        sanitize_item = cls.sanitize(item)
        return Ticket(**sanitize_item)


    @staticmethod
    def asdict(ticket: Ticket | PartialTicket) -> dict:
        if isintance(ticket, Ticket):
            return ticket._asdict()
        return {k: v for k, v in ticket._asdict().items() if k is not None}


    #Test
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
