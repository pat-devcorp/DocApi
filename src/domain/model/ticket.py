from collections import namedtuple
import json
from enum import Enum

from pydantic import BaseModel
from validator_collection.checkers import is_not_empty

from ..IdentifierHandler import IdentifierHandler, IdentityAlgorithm
from ...utils.DatetimeHandler import checkDatetimeFormat
from ..SchemaItemHandler import SchemaItemHandler
from ...domain.DomainError import DomainError
from ...infrastructure.InfrastructureError import InfrastructureError
from ...utils.AuditHandler import AuditHandler


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
    ticketId: str | TicketIdentifier
    description: str
    category: int | TicketCategory
    typeCommit: int | TicketTypeCommit
    state: int | TicketState
    points: int
    estimateEndAt: str 

    @staticmethod
    def getSchema() -> str:
        json_obj = {
            "ticketId": SchemaItemHandler(1, 0, "String"),
            "description": SchemaItemHandler(1, 1, "String"),
            "category": SchemaItemHandler(0, 1, "Enum", TicketCategory.UNDEFINED.value, TicketCategory),
            "typeCommit": SchemaItemHandler(0, 1, "Enum", TicketTypeCommit.UNDEFINED.value, TicketTypeCommit),
            "state": SchemaItemHandler(0, 1, "Enum", TicketState.CREATED.value, TicketState),
            "points": SchemaItemHandler(0, 1, "int", 0),
            "estimateEndAt": SchemaItemHandler(0, 1, "String", None)
        }
        return {k:v.model_dump_json() for k, v in json_obj}

    @staticmethod
    def getFields():
        ["ticketId", "description", "category", "typeCommit", "state", "points", "estimateEndAt"]

    def asDict(self) -> dict:
        data = dict()
        for item in self.getFields():
            val = self.__getattribute__(item)
            data[item] = val if isinstance(val, (str, int)) else val.value
    
    def __str__(self):
        return json.dumps(self.asDict())

    def __repr__(self):
        return self.__str__()


# Schema validation
class TicketDto(Ticket):
    @classmethod
    def getMock(cls) -> None:
        identity = TicketIdentifier("873788d4-894c-11ee-b9d1-0242ac120002")
        return cls(ticketId=identity, description="Test task")
    

    @classmethod
    def isValid(cls, ref_object: dict, is_partial=True) -> tuple[bool, str]:
        validate_func = {
            "ticketId": cls.isValidId,
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
            if func := validate_func.get(k):
                is_ok, err = func(v)
                if not is_ok:
                    errors.append(err)

        if len(errors) > 0:
            return False, "\n".join(errors)

        return True, ""

    @staticmethod
    def isValidId(ticketId: str) -> tuple(bool, str):
        try:
            TicketIdentifier(ticketId)
            return True, ""
        except ValueError:
            return False, "Invalid id"

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
        if not is_not_empty(description, maximum_length=200):
            return False, "Max length exceeded, not allowed"
        return True, ""

    @staticmethod
    def isValidEndAt(estimateEndAt: str) -> tuple[bool, str]:
        if not checkDatetimeFormat(estimateEndAt):
            return False, "Date of end format not valid"
        return True, ""

    @classmethod
    def fromDict(cls, params: dict) -> None | DomainError:
        data = {k: params.get(k, None) for k in cls.getFields()}
        return cls(**data)
    

    def __init__(
        self,
        ticketId: str,
        description: str | None,
        category: int | None,
        typeCommit: int | None,
        state: int | None,
        points: int | None,
        estimateEndAt: str | None
    ) -> None | DomainError:
        Ticket.__init__(
            ticketId,
            description,
            category,
            typeCommit,
            state,
            points,
            estimateEndAt
        )
    
        is_ok, err = self.isValid(self.asDict(), False)
        if not is_ok:
            raise DomainError("DTO_VALIDATION", "\n".join(err))
    
    def asDict(self) -> dict:
        return self._obj._asDict()
    
    def __str__(self):
        return json.dumps(self.asDict())

    def __repr__(self):
        return self.__str__()


# Domain
class TicketDao(Ticket):
    @classmethod
    def getMock(cls):
        identity = IdentifierHandler("87378618-894c-11ee-b9d1-0242ac120002")
        return cls(
            ticketId=identity,
            description="Test task",
        )
    
    def fromDict(self, data: dict):
        # data.ticketId = TicketIdentifier(data.ticketId)
        data.category = TicketCategory(data.category)
        data.typeCommit = TicketTypeCommit(data.typeCommit)
        data.state =  TicketState(data.state)
        self._obj = Ticket(**data)

    def __init__(
        self,
        ref_write_uid,
        ref_repository,
    ) -> None:
        self._r = ref_repository
        self._w = ref_write_uid
        self._fields = list(Ticket._fields()) + list(AuditHandler.getFields())
    
    def toRepository(self) -> dict:
        data = self._obj._asDict()
        for field in ["ticketId", "category", "typeCommit", "state"]:
            data.update(field, data[field].value)
        return data

    def __str__(self):
        return json.dumps(self.asDict())

    def __repr__(self):
        return self.__str__()
    
    def setFields(self, fields: list) -> None:
        self._fields = [field for field in fields if field in TicketDao.getFields()]

    def fetch(self) -> list:
        return self._r.fetch(self._fields)
    
    def create(self, ref_dto) -> None | InfrastructureError:
        data = dict()

        data.update(AuditHandler.getCreateFields(self._w))

        return self._r.create(data)

    def update(self, ref_dto) -> None | InfrastructureError:
        data = dict()

        data.update(AuditHandler.getUpdateFields(self._w))

        return self._r.update(data)

    def getById(self, objId: TicketIdentifier):
        return self._r.getById(objId.value, self._fields)
    
    def delete(self, objId: TicketIdentifier):
        audit = AuditHandler.getUpdateFields(self._w)
        self._r.update(audit)

        return self._r.delete(objId.value)