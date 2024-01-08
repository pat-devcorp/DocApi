from ..infrastructure.providers.User import UserService
from ..domain.IdentifierHandler import IdentifierHandler, IdentityAlgorithm
from .DatetimeHandler import getDatetime, checkDatetimeFormat
from .HandlerError import HandlerError
from .ResponseHandler import FORMAT_NOT_MATCH, ID_NOT_FOUND, WRITE_UID_NOT_FOUND


class AuditHandler:
    @staticmethod
    def getFields():
        return ["write_uid", "write_at", "create_uid", "create_at", "end_at"]

    @staticmethod
    def getMock():
        return {
            "write_uid": UserService.getMock(),
            "write_at": getDatetime(),
            "create_uid": UserService.getMock(),
            "create_at": getDatetime(),
            "end_at": getDatetime(),
        }

    def isValid(cls, my_audit: dict) -> list:
        errors = list()

        if my_audit.get("create_uid") is None:
            errors.append("Create User is required")

        my_write_at = my_audit.get("write_at")
        if my_write_at is not None:
            if not checkDatetimeFormat(my_write_at):
                errors.append(FORMAT_NOT_MATCH)

        my_create_at = my_audit.get("create_at")
        if my_create_at is not None:
            if not checkDatetimeFormat(my_create_at):
                errors.append(FORMAT_NOT_MATCH)

        my_create_at = my_audit.get("end_at")
        if my_create_at is not None:
            if not checkDatetimeFormat(my_create_at):
                errors.append(FORMAT_NOT_MATCH)

        return errors

    @classmethod
    def getIdentifier(cls, user_id):
        if not UserService.isValidUserId(user_id):
            raise HandlerError(ID_NOT_FOUND)
        return IdentifierHandler(IdentityAlgorithm.DEFAULT, user_id)

    @classmethod
    def fromDict(cls, params: dict):
        if params.get("write_uid") is None:
            raise HandlerError(WRITE_UID_NOT_FOUND)

        if not UserService.isValidUserId(params.get("write_uid")):
            raise HandlerError(ID_NOT_FOUND)

        audit_dto = dict()
        for k in cls.getFields():
            audit_dto[k] = params[k] if params.get(k) is not None else None

        errors = cls.isValid(params)
        if len(errors) > 0:
            raise HandlerError("\n".join(errors))

        return audit_dto

    @classmethod
    def getUpdateFields(cls, current_uid):
        if not UserService.isValidUserId(current_uid):
            raise HandlerError(ID_NOT_FOUND)
        return {"write_uid": current_uid, "write_at": getDatetime()}

    @classmethod
    def getCreateFields(cls, current_uid):
        if not UserService.isValidUserId(current_uid):
            raise HandlerError(ID_NOT_FOUND)
        return {
            "write_uid": current_uid,
            "write_at": getDatetime(),
            "create_uid": current_uid,
            "create_at": getDatetime(),
            "end_at": None,
        }

    @classmethod
    def getEndFields(cls, current_uid):
        if not UserService.isValidUserId(current_uid):
            raise HandlerError(ID_NOT_FOUND)
        return {
            "write_uid": current_uid,
            "write_at": getDatetime(),
            "end_at": getDatetime(),
        }
