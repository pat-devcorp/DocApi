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


class TicketIdentifier:
    ticketId: str

    @staticmethod
    def getIdAlgorithm():
        return IdentityAlgorithm.UUid_V4

    @classmethod
    def getIdentifier(cls, self):
        identifier = IdentifierHandler(cls.getIdAlgorithm())
        return cls(identifier.getDefault())

    def __init__(self, ticketId) None | ValueError:
        identifier = IdentifierHandler(cls.getIdAlgorithm())
        self.ticketId = identifier.setIdentifier(ticketId)


Ticket = namedtuple("Ticket", ["ticketId", "description", "category", "typeCommit", "state", "points", "estimateEndAt"])


# Schema validation
class TicketDto:
    @classmethod
    def getMock(cls):
        identity = cls.getIdentifier("873788d4-894c-11ee-b9d1-0242ac120002")
        return cls(ticketId=identity, description="Test task")
    
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
    def isValid(cls, ref_object: dict, is_partial=True) -> tuple[bool, str]:
        validate_funcs = {
            "ticketId": cls.isValidid,
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
            if func := validate_funcs.get(k):
                is_ok, err = func(v)
                if not is_ok:
                    errors.append(err)

        if len(errors) > 0:
            return False, "\n".join(errors)

        return True, ""

    @staticmethod
    def isValidid(ticketId: str) -> tuple(bool, str):
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
        if not is_not_empty(description, maximum_lengt=200):
            return False, "Max length exceeded, not allowed"
        return True, ""

    @staticmethod
    def isValidEndAt(estimateEndAt: str) -> tuple[bool, str]:
        if not valdiateDatetimeFormat(estimateEndAt):
            return False, "Date of end format not valid"
        return True, ""

    @classmethod
    def fromDict(cls, params: dict) -> None | PresentationError:
        data = {k: params.get(k, None) for k in cls.getFields()}
        return cls(**data)
    

    def __init__(
        self,
        ticketId: str,
        description: str | None,
        category: int | None,
        typeCommit: int | None,
        state: int | None
        points: int | None
        estimateEndAt: str | None
    ) -> None | PresentationError:
        self._obj = Ticket(
            ticketId,
            description,
            category,
            typeCommit,
            state,
            points,
            estimateEndAt
        )
    
        is_ok, err = self.isValid(self.obj._asDict(), False)
        if not is_ok:
            raise PresentationError(PRESENTATION_VALidATION, "\n".join(err))
    
    def asDict(self):
        return self._obj._asDict()
    
    def __str__(self):
        return json.dumps(self.asDict())

    def __repr__(self):
        return self.__str__()


# Domain
class TicketDao:
    @classmethod
    def getMock(cls):
        identity = IdentityHandler("87378618-894c-11ee-b9d1-0242ac120002")
        return cls(
            ticketId=identity,
            description="Test task",
        )


    @classmethod
    def getById(cls, ref_repository: RepositoryProtocol, objId: TicketIdentifier):
        return ref_repository.getById(objId.value, self._fields)
    
    @classmethod
    def delete(cls, write_uid, ref_repository: RepositoryProtocol, objId: TicketIdentifier):
        audit = AuditHandler.getUpdateFields(self._write_uid)
        ref_repository.update(audit)

        return ref_repository.delete(objId.value)

    @classmethod
    def fromRepository(cls, write_uid, ref_repository: RepositoryProtocol, objId: IdentifierHandler):
        obj =  ref_repository.getById(objId.value, cls._fields)
        dto = TicketDto.fromDict(**obj)
        return cls(write_uid, ref_repository, dto)


    def __init__(
        self,
        ref_write_uid,
        ref_repository: RepositoryProtocol,
        ref_dto: TicketDto
    ):
        data = ref_dto._asDict()
        data.ticketId = IdentityHandler(data.ticketId)
        data.category = TicketCategory(data.category)
        data.typeCommit = TicketTypeCommit(data.typeCommit)
        data.state =  TicketState(data.state)
        self._obj = Ticket(**data)

        self._r = ref_repository
        self._write_uid = ref_write_uid
        self._fields = list(Ticket._fields()) + list(AuditHandler.getFields())
    
    def asDict(self) -> dict:
        data = self._obj._asDict()
        for field in ["ticketId", "category", "typeCommit", "state"]:
            data[field] = val.value
        return data

    def __str__(self):
        return json.dumps(self.asDict())

    def __repr__(self):
        return self.__str__()
    
    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in TicketDao.getFields()]

    def fetch(self) -> list:
        return self._r.fetch(self._fields)
    
    def create(self) -> bool:
        data = self_dto.asDict()
        data.update(AuditHandler.getCreateFields(self._write_uid))

        return self._r.create(data)

    def update(self) -> bool:
        data = self_dto.asDict()
        data.update(AuditHandler.getUpdateFields(self._write_uid))

        return self._r.update(data)