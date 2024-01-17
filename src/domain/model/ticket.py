import json
from enum import Enum

from ...domain.DomainError import DomainError
from ...utils.DatetimeHandler import DateTimeHandler, checkDatetimeFormat
from ...utils.ResponseHandler import SCHEMA_NOT_MATCH
from ...utils.StrHandler import valMaxLength
from ..IdentifierHandler import IdentifierHandler, IdentityAlgorithm


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
            "description": cls.isValidDescription,
            "category": cls.isValidCategory,
            "typeCommit": cls.isValidTypeCommit,
            "state": cls.isValidState,
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
    def isValidState(state: int) -> tuple[bool, str]:
        for member in TicketState:
            if member.value == state:
                return True, ""
        return False, "Invalid state"

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
        if not valMaxLength(description, maximum_length=200):
            return False, "Max length exceeded, not allowed"
        return True, ""

    @staticmethod
    def isValidEndAt(estimateEndAt: str) -> tuple[bool, str]:
        if not checkDatetimeFormat(estimateEndAt):
            return False, "Date of end format not valid"
        return True, ""


class TicketIdentifier:
    value: str

    @staticmethod
    def getIdAlgorithm():
        return IdentityAlgorithm.UUid_V4

    @classmethod
    def getIdentifier(cls):
        identifier = IdentifierHandler(cls.getIdAlgorithm())
        return cls(identifier.getDefault())

    def __init__(self, value) -> None | ValueError:
        identifier = IdentifierHandler(self.getIdAlgorithm())
        self.value = identifier.setIdentifier(value)


class Ticket:
    ticketId: TicketIdentifier
    description: str
    category: TicketCategory
    typeCommit: TicketTypeCommit
    state: TicketState
    points: int
    estimateEndAt: DateTimeHandler

    @staticmethod
    def getFields():
        return [
            "ticketId",
            "description",
            "category",
            "typeCommit",
            "state",
            "points",
            "estimateEndAt",
        ]

    def asDict(self) -> dict:
        data = dict()
        for item in self.getFields():
            val = self.__getattribute__(item)
            data[item] = val if isinstance(val, (str, int)) else val.value

    def __str__(self):
        return json.dumps(self.asDict())

    def __repr__(self):
        return self.__str__()

    @classmethod
    def newTicket(
        cls, ticketId: TicketIdentifier, description: str
    ) -> None | DomainError:
        is_ok, err = TicketValidator.isValidDescription(description)
        if not is_ok:
            raise DomainError(SCHEMA_NOT_MATCH, err)

        return cls(
            ticketId,
            description,
            TicketCategory.PENDENTS,
            TicketTypeCommit.UNDEFINED,
            TicketState.CREATED,
            0,
            DateTimeHandler.getDefault(),
        )

    @classmethod
    def fromDict(cls, item: dict):
        TicketValidator.isValid(item, False)
        return cls(
            item["ticketId"],
            item["description"],
            TicketCategory(item["category"]),
            TicketTypeCommit(item["typeCommit"]),
            TicketState(item["state"]),
            item["points"],
            DateTimeHandler.fromStr(item["estimateEndAt"]),
        )

    def __init__(
        self,
        ticketId: str,
        description: str,
        category: TicketCategory,
        typeCommit: TicketTypeCommit,
        state: TicketState,
        points: int,
        estimateEndAt: DateTimeHandler,
    ) -> None:
        self.ticketId = TicketIdentifier(ticketId)
        self.description = description
        self.category = category
        self.typeCommit = typeCommit
        self.state = state
        self.points = points
        self.estimateEndAt = estimateEndAt
