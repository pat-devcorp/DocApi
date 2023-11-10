from collections import namedtuple
from enum import Enum
from typing import Tuple
from validator_collection import checkers

from ...utils.ErrorHandler import REQUIRED_FIELD
from ...utils.DatetimeHandler import valdiateDatetimeFormat
from ...utils.IdentityHandler import IdentityAlgorithm, IdentityHandler
from ..DomainError import DomainError


class TicketCategory(Enum):
    UNDEFINED = 0
    HOTFIX = 1
    BUGFIX = 2
    FEATURE = 3
    REFACTOR = 4
    DOCS = 5


class TicketState(Enum):
    CREATED = 0
    DELETED = 1
    IN_PROCESS = 2
    OBSERVE = 3
    END = 4


class EnsureTicket:
    @staticmethod
    def getFields() -> list:
        return ["ticket_id", "description", "category", "state", "end_at"]

    @staticmethod
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
        data = dict()
        for k in cls.getFields():
            if params.get(k) is None:
                raise DomainError(REQUIRED_FIELD)
            data[k] = params[k]
        return data

    @classmethod
    def partialValidate(cls, ref_object: dict) -> str:
        validate_funcs = {
            "ticket_id": cls.isValidTicketId,
            "description": cls.isValidDescription,
            "category": cls.isValidCategory,
            "state": cls.isValidState,
            "end_at": cls.isValidEndAt,
        }

        ticket = {k: v for k, v in ref_object.items() if k in validate_funcs.keys()}

        errors = list()
        for k, v in ticket.items():
            func = validate_funcs[k]
            is_ok, err = func(v)
            if not is_ok:
                errors.append(err)

        if len(errors) > 0:
            return "\n".join(errors)

        return ""

    @staticmethod
    def isValidTicketId(ticket_id: str) -> Tuple[bool, str]:
        if not IdentityHandler.isValid(ticket_id, IdentityAlgorithm.UUID_V4):
            return False, "Identity not valid for ticket"
        return True, ""

    @staticmethod
    def isValidState(state: str) -> Tuple[bool, str]:
        for member in TicketState:
            if member.value == state:
                return True, ""
        return False, "Invalid state"

    @staticmethod
    def isValidCategory(category: str) -> Tuple[bool, str]:
        for member in TicketCategory:
            if member.value == category:
                return True, ""
        return False, "Invalid state"

    @staticmethod
    def isValidDescription(description: str) -> Tuple[bool, str]:
        if not checkers.is_string(description, maximum_lengt=200):
            return False, "Max length exceeded, not allowed"
        return True, ""

    @staticmethod
    def isValidEndAt(end_at) -> Tuple[bool, str]:
        if not valdiateDatetimeFormat(end_at):
            return False, "Date of end format not valid"
        return True, ""

    @classmethod
    def getIdentifier(cls, identifier):
        cls.isValidTicketId(identifier)
        return IdentityHandler(IdentityAlgorithm.UUID_V4, identifier)
