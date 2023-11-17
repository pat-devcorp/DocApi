from enum import Enum

from validator_collection.checkers import is_not_empty

from ...domain.IdentityHandler import IdentityHandler
from ...presentation.IdentifierHandler import IdentifierHandler, IdentityAlgorithm
from ...utils.DatetimeHandler import valdiateDatetimeFormat


class TicketCategory(Enum):
    UNDEFINED = 0
    PENDIENTES = 1
    SOPORTE = 2
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


class ValidTicket:
    @classmethod
    def isValid(cls, ref_object: dict, is_partial=True) -> tuple[bool, str]:
        validate_funcs = {
            "description": cls.isValidDescription,
            "category": cls.isValidCategory,
            "type_commit": cls.isValidTypeCommit,
            "state": cls.isValidState,
            "estimate_end_at": cls.isValidEndAt,
        }

        errors = list()
        for k, v in ref_object.items():
            if is_partial and v is None:
                continue
            if func := validate_funcs.get(k):
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
    def isValidTypeCommit(type_commit: int) -> tuple[bool, str]:
        for member in TicketTypeCommit:
            if member.value == type_commit:
                return True, ""
        return False, "Invalid commit type"

    @staticmethod
    def isValidDescription(description: str) -> tuple[bool, str]:
        if not is_not_empty(description, maximum_lengt=200):
            return False, "Max length exceeded, not allowed"
        return True, ""

    @staticmethod
    def isValidEndAt(estimate_end_at: str) -> tuple[bool, str]:
        if not valdiateDatetimeFormat(estimate_end_at):
            return False, "Date of end format not valid"
        return True, ""


class TicketDAO:
    ticket_id: IdentityHandler
    description: str
    category: int
    type_commit: int
    state: int
    points: int = (0,)
    estimate_end_at: str | None = (None,)

    def toRepository(self) -> dict:
        data = dict()
        for field in self.getFields():
            value = self.__getattribute__(field)
            if value is not None:
                data[field] = value
        return data

    @staticmethod
    def getIdAlgorithm():
        return IdentityAlgorithm.UUID_V4

    @staticmethod
    def getIdentifier(identifier: str):
        pk = IdentifierHandler(TicketDAO.getIdAlgorithm())
        pk.setIdentifier(identifier)
        return pk

    @classmethod
    def getMock(cls) -> dict:
        return {
            "ticket_id": cls.getIdentifier("3ca3d2c3-01bb-443e-afb8-7aac10d40f9c"),
            "description": "Test task",
            "category": TicketCategory.UNDEFINED,
            "type_commit": TicketTypeCommit.UNDEFINED,
            "state": TicketState.CREATED,
            "points": 0,
            "estimate_end_at": "2023/20/10 10:10",
        }

    def __init__(
        self,
        ticket_id: IdentityHandler,
        description: str,
        category: TicketCategory = TicketCategory.UNDEFINED,
        type_commit: TicketTypeCommit = TicketTypeCommit.UNDEFINED,
        state: TicketState = TicketState.CREATED,
        points: int = 0,
        estimate_end_at: str | None = None,
    ):
        self.ticket_id = ticket_id
        self.description = description
        self.category = category
        self.type_commit = type_commit
        self.state = state
        self.points = points
        self.estimate_end_at = estimate_end_at

    @classmethod
    def fromDict(cls, ticket_id: IdentityHandler, params: dict):
        ticket = {k: params.get(k, None) for k in cls.getFields()}
        return cls(ticket_id, **ticket)

    @staticmethod
    def getFields() -> list:
        return [
            "ticket_id",
            "description",
            "category",
            "type_commit",
            "state",
            "points",
            "estimate_end_at",
        ]
