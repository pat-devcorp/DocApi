import json
from enum import Enum
from pydantic import BaseModel

from validator_collection.checkers import is_not_empty

from ...domain.IdentityHandler import IdentityHandler
from ...presentation.IdentifierHandler import IdentityAlgorithm
from ...utils.DatetimeHandler import valdiateDatetimeFormat
from ..SchemaHandler import SchemaHandler


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
        if not is_not_empty(description, maximum_lengt=200):
            return False, "Max length exceeded, not allowed"
        return True, ""

    @staticmethod
    def isValidEndAt(estimateEndAt: str) -> tuple[bool, str]:
        if not valdiateDatetimeFormat(estimateEndAt):
            return False, "Date of end format not valid"
        return True, ""


class TicketDAO(BaseModel):
    ticketId: IdentityHandler
    description: str
    category: TicketCategory
    typeCommit: TicketTypeCommit
    state: TicketState
    points: int = (0,)
    estimateEndAt: str | None = (None,)


    def asDict(self) -> dict:
        data = dict()
        special_keys = ["ticketId", "category", "typeCommit", "state"]
        for field in self.getFields():
            val = self.__getattribute__(field)
            if val is not None:
                data[field] = val if field not in special_keys else val.value
        return data

    @staticmethod
    def getIdAlgorithm():
        return IdentityAlgorithm.UUID_V4

    @staticmethod
    def getFields() -> list:
        return [
            "ticketId",
            "description",
            "category",
            "typeCommit",
            "state",
            "points",
            "estimateEndAt",
        ]

    @staticmethod
    def getSchema():
        json_obj = {
            "ticketId": SchemaHandler(1, 0, "String"),
            "description": SchemaHandler(1, 1, "String"),
            "category": SchemaHandler(0, 1, "Enum", TicketCategory.UNDEFINED.value, TicketCategory),
            "typeCommit": SchemaHandler(0, 1, "Enum", TicketTypeCommit.UNDEFINED.value, TicketTypeCommit),
            "state": SchemaHandler(0, 1, "Enum", TicketState.CREATED.value, TicketState),
            "points": SchemaHandler(0, 1, "int", 0),
            "estimateEndAt": SchemaHandler(0, 1, "String", None)
        }
        return {k:v.model_dump_json() for k, v in json_obj}
    
    @classmethod
    def getMock(cls):
        identity = IdentityHandler("87378618-894c-11ee-b9d1-0242ac120002")
        return cls(
            ticketId=identity,
            description="Test task",
        )

    def __str__(self):
        return json.dumps(self.asDict())

    def __repr__(self):
        return self.__str__()


    def __init__(
        self,
        ticketId: IdentityHandler,
        description: str,
        category: TicketCategory = TicketCategory.UNDEFINED,
        typeCommit: TicketTypeCommit = TicketTypeCommit.UNDEFINED,
        state: TicketState = TicketState.CREATED,
        points: int = 0,
        estimateEndAt: str | None = None,
    ):
        self.ticketId = ticketId
        self.description = description
        self.category = category
        self.typeCommit = typeCommit
        self.state = state
        self.points = points
        self.estimateEndAt = estimateEndAt


    def updatedObj(
        self,
        ticketId: IdentityHandler,
        description: str | None,
        category: TicketCategory | None,
        typeCommit: TicketTypeCommit | None,
        state: TicketState | None,
        points: int | None,
        estimateEndAt: str | None
    ):
        self.ticketId = ticketId
        self.description = description
        self.category = category
        self.typeCommit = typeCommit
        self.state = state
        self.points = points
        self.estimateEndAt = estimateEndAt

    @classmethod
    def filterKeys(cls, params: dict) -> dict:
        return ticket = {k: params.get(k, None) for k in cls.getFields()}


    @staticmethod
    def isValid(ref_object: dict, is_partial=True) -> tuple[bool, str]:
        validate_funcs = {
            "description": ValidTicket.isValidDescription,
            "category": ValidTicket.isValidCategory,
            "typeCommit": ValidTicket.isValidTypeCommit,
            "state": ValidTicket.isValidState,
            "estimateEndAt": ValidTicket.isValidEndAt,
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