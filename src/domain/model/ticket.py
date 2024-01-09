from collections import namedtuple
import json
from enum import Enum

from pydantic import BaseModel
from validator_collection.checkers import is_not_empty

from ..IdentifierHandler import IdentifierHandler, IdentityAlgorithm
from ...utils.DatetimeHandler import checkDatetimeFormat, getDatetime
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
    ticketId: TicketIdentifier
    description: str
    category: TicketCategory
    typeCommit:  TicketTypeCommit
    state: TicketState
    points: int
    estimateEndAt: str

    @staticmethod
    def getFields():
        return ["ticketId", "description", "category", "typeCommit", "state", "points", "estimateEndAt"]

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
    def newTicket(cls, ticketId, description) -> None | DomainError:
        return cls(
            ticketId,
            description,
            TicketCategory.PENDENTS,
            TicketTypeCommit.UNDEFINED,
            TicketState.CREATED,
            0,
            getDatetime()
        )