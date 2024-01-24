from collections import namedtuple
from enum import Enum

from ...domain.DomainError import DomainError
from ...utils.DatetimeHandler import DateTimeHandler, checkDatetimeFormat
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
    @classmethod
    def isValid(cls, ref_object: dict, is_partial=True) -> tuple[bool, str]:
        validate_func = {
            "ticketId": cls.isValidIdentifier,
            "description": cls.isValidDescription,
            "category": cls.isValidCategory,
            "typeCommit": cls.isValidTypeCommit,
            "state": cls.isValidState,
            "points": cls.isValidPoints,
            "estimateEndAt": cls.isValidEndAt,
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
    def isValidIdentifier(identifier: str):
        try:
            TicketInterface.setIdentifier(identifier)
            return True, ""
        except DomainError:
            return False, "Invalid identifier"

    @staticmethod
    def isValidState(state: int) -> tuple[bool, str]:
        for member in TicketState:
            if member.value == state:
                return True, ""
        return False, "Invalid state"

    @staticmethod
    def isValidPoints(points: int):
        if points > 0 and points < 11:
            return False, "Invalid points, be more than 0 and less than ten"
        return True, ""

    @staticmethod
    def isValidCategory(category: int) -> tuple[bool, str]:
        for member in TicketCategory:
            if member.value == category:
                return True, ""
        return False, "Invalid category"

    @staticmethod
    def isValidTypeCommit(typeCommit: int) -> tuple[bool, str]:
        for member in TicketTypeCommit:
            if member.value == typeCommit:
                return True, ""
        return False, "Invalid commit type"

    @staticmethod
    def isValidDescription(description: str) -> tuple[bool, str]:
        maximum_length = 200
        if isinstance(description, str) and (
            maximum_length is None or len(description) <= maximum_length
        ):
            return True, ""
        return False, "is empty or max length exceeded, not allowed"

    @staticmethod
    def isValidEndAt(estimateEndAt: str) -> tuple[bool, str]:
        if not checkDatetimeFormat(estimateEndAt):
            return False, "Date of end format not valid"
        return True, ""


class TicketInterface:
    _idAlgorithm = IdentityAlgorithm.UUID_V4

    @classmethod
    def getIdentifier(cls) -> TicketIdentifier:
        ic = IdentifierHandler.getDefault(cls._idAlgorithm)
        return TicketIdentifier(ic)

    @classmethod
    def setIdentifier(cls, identifier) -> TicketIdentifier | DomainError:
        is_ok, err = IdentifierHandler.isValid(identifier, cls._idAlgorithm)
        if not is_ok:
            raise DomainError(ID_NOT_VALID, err)
        return TicketIdentifier(identifier)

    @classmethod
    def fromDict(cls, data: dict) -> Ticket | DomainError:
        item = {k: v for k, v in data if k in Ticket._fields}
        ok, err = TicketValidator.isValid(item, False)
        if not ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)
        return Ticket(
            item["ticketId"],
            item["description"],
            item["category"],
            item["typeCommit"],
            item["state"],
            item["points"],
            item["estimateEndAt"],
        )

    @classmethod
    def validDict(cls, data: dict) -> dict | DomainError:
        item = {k: v for k, v in data if k in Ticket._fields}
        ok, err = TicketValidator.isValid(item)
        if not ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)
        return item

    @classmethod
    def newTicket(
        cls, identifier: TicketIdentifier, description: str
    ) -> Ticket | DomainError:
        is_ok, err = TicketValidator.isValidDescription(description)
        if not is_ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)

        return Ticket(
            identifier.value,
            description,
            TicketCategory.PENDENTS.value,
            TicketTypeCommit.UNDEFINED.value,
            TicketState.CREATED.value,
            1,
            DateTimeHandler.now().value,
        )

    @staticmethod
    def badTicket() -> Ticket:
        return Ticket(
            "a",
            "a" * 201,
            100,
            100,
            100,
            100,
            "20/20/20",
        )
