from enum import Enum

from validator_collection import checkers

from ..utils.DatetimeHandler import valdiateDateFormat
from ..utils.IdentityHandler import IdentityAlgorithm, IdentityHandler
from .DomainError import DomainError


class MemberRole(Enum):
    MEMBER: 0


class Member:
    @staticmethod
    def getFields() -> list:
        return ["member_id", "role_id"]

    @classmethod
    def getMock():
        return {"member_id": 0, "role_id": 0}

    @classmethod
    def domainFilter(cls, params: dict, is_partial=True) -> dict:
        if is_partial:
            return {
                k: v
                for k, v in params.items()
                if k in cls.getFields() and v is not None
            }
        if params.keys() != cls.getFields():
            raise DomainError("Fail to create meeting")
        data = dict()
        for k in cls.getFields():
            if params.get(k) is None:
                raise DomainError(f"{k}: must be present in meeting")
            data[k] = params[k]
        return data

    @classmethod
    def partialValidate(cls, ref_object: dict) -> str:
        print("---DOMAIN---")
        print(ref_object)
        validate_funcs = {
            "member_id": cls.validateIdentifier,
            "role_id": cls.validateRole,
        }

        meeting = {k: v for k, v in ref_object.items() if k in validate_funcs.keys()}

        errors = list()
        for k, v in meeting.items():
            func = validate_funcs[k]
            err = func(v)
            if len(err) > 0:
                errors.append(err)

        if len(errors) > 0:
            return "\n".join(errors)

        return None

    @staticmethod
    def validateIdentifier(ticket_id: str) -> str:
        if not IdentityHandler.validate(ticket_id, IdentityAlgorithm.DEFAULT):
            return "Identity not valid for meeting"
        return ""

    @staticmethod
    def validateRole(category: str) -> str:
        for member in MemberRole:
            if member.value == category:
                return ""
        return "Invalid state"
