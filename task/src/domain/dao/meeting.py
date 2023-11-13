from validator_collection import checkers

from ...utils.DatetimeHandler import valdiateDateFormat
from ...utils.IdentityHandler import IdentityAlgorithm, IdentityHandler
from ..DomainError import DomainError


class EnsureMeeting:
    @staticmethod
    def getFields() -> list:
        return ["meeting_id", "subject", "meet_date"]

    @classmethod
    def getMock():
        return {"meeting_id": 0, "subject": "Test task", "meet_date": "2023/04/01"}

    @classmethod
    def filterKeys(cls, params: dict, is_partial=True) -> dict:
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
    def isValid(cls, ref_object: dict) -> str:
        print("---DOMAIN---")
        print(ref_object)
        validate_funcs = {
            "ticket_id": cls.isValidIdentifier,
            "description": cls.validateDescription,
            "meet_date": cls.validateMeetDate,
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
    def isValidIdentifier(ticket_id: str) -> str:
        if not IdentityHandler.isValid(ticket_id, IdentityAlgorithm.DEFAULT):
            return False, "Identity not valid for meeting"
        return True, ""

    @staticmethod
    def isValidDescription(description: str) -> str:
        if not checkers.is_string(description, maximum_lengt=200):
            return False, "Max length exceeded, not allowed"
        return True, ""

    @staticmethod
    def isValidMeetDate(end_at) -> str:
        if not valdiateDateFormat(end_at):
            return False, "Date of end format not valid"
        return True, ""
