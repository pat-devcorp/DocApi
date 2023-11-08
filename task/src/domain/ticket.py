from collections import namedtuple
from enum import Enum

from validator_collection import checkers

from ..domain.DomainError import DomainError
from ..utils.DatetimeHandler import valdiateDatetimeFormat
from ..utils.IdentityHandler import IdentityAlgorithm, IdentityHandler


class TicketCategory(Enum):
    UNDEFINED = 0
    HOTFIX = 1
    BUGFIX = 2
    FEATURE = 3
    REFACTOR = 4
    DOCS = 5


class TicketState(Enum):
    UNDIFINED = 0
    DELETED = 1
    CREATED = 2
    IN_PROCESS = 3
    OBSERVE = 4
    END = 5


class EnsureTicket:
    @staticmethod
    def getFields() -> list:
        return ["ticket_id", "description", "category", "state", "end_at"]

    @classmethod
    def getMock():
        return {
            "ticket_id": "3ca3d2c3-01bb-443e-afb8-7aac10d40f9c",
            "description": "Test task",
            "category": 0,
            "state": 0,
            "events": "2023/07/18 14:00",
            "points": 0,
        }

    @classmethod
    def domainFilter(cls, params: dict, is_partial=True) -> dict:
        if is_partial:
            return {
                k: v
                for k, v in params.items()
                if k in cls.getFields() and v is not None
            }
        if params.keys() != cls.getFields():
            raise DomainError("Fail to create ticket")
        data = dict()
        for k in cls.getFields():
            if params.get(k) is None:
                raise DomainError(f"{k}: must be present in ticket")
            data[k] = params[k]
        return data

    @classmethod
    def partialValidate(cls, ref_object: dict) -> str:
        validate_funcs = {
            "ticket_id": cls.validateTicketId,
            "description": cls.validateDescription,
            "category": cls.validateCategory,
            "state": cls.validateState,
            "end_at": cls.validateEndAt,
        }

        ticket = {k: v for k, v in ref_object.items() if k in validate_funcs.keys()}

        errors = list()
        for k, v in ticket.items():
            func = validate_funcs[k]
            err = func(v)
            if len(err) > 0:
                errors.append(err)

        if len(errors) > 0:
            return "\n".join(errors)

        return None

    @staticmethod
    def validateTicketId(ticket_id: str) -> str:
        if not IdentityHandler.validate(ticket_id, IdentityAlgorithm.UUID_V4):
            return "Identity not valid for ticket"
        return ""

    @staticmethod
    def validateState(state: str) -> str:
        for member in TicketState:
            if member.value == state:
                return ""
        return "Invalid state"

    @staticmethod
    def validateCategory(category: str) -> str:
        for member in TicketCategory:
            if member.value == category:
                return ""
        return "Invalid state"

    @staticmethod
    def validateDescription(description: str) -> str:
        if not checkers.is_string(description, maximum_lengt=200):
            return "Max length exceeded, not allowed"
        return ""

    @staticmethod
    def validateEndAt(end_at) -> str:
        if not valdiateDatetimeFormat(end_at):
            return "Date of end format not valid"
        return ""

    @classmethod
    def getIdentifier(cls, identifier):
        cls.validateTicketId(identifier)
        return IdentityHandler(IdentityAlgorithm.UUID_V4, identifier)
