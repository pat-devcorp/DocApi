from validator_collection import checkers

from ..utils.IdentityHandler import IdentityAlgorithm, IdentityHandler
from .DomainError import DomainError


class EnsureKeyword:
    @staticmethod
    def getFields() -> list:
        return ["keyword_id", "description"]

    @classmethod
    def getMock():
        return {
            "ticket_id": 0,
            "description": "Test task",
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
            raise DomainError("Fail to create keyword")
        data = dict()
        for k in cls.getFields():
            if params.get(k) is None:
                raise DomainError(f"{k}: must be present in keyword")
            data[k] = params[k]
        return data

    @classmethod
    def partialValidate(cls, ref_object: dict) -> str:
        print("---DOMAIN---")
        print(ref_object)
        validate_funcs = {
            "ticket_id": cls.validateIdentifier,
            "description": cls.validateDescription,
        }

        keyword = {k: v for k, v in ref_object.items() if k in validate_funcs.keys()}

        errors = list()
        for k, v in keyword.items():
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
            return "Identity not valid for keyword"
        return ""

    @staticmethod
    def validateDescription(description: str) -> str:
        if not checkers.is_string(description, maximum_lengt=200):
            return "Max length exceeded, not allowed"
        return ""
