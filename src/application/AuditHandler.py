from ..domain.IdentifierHandler import IdentifierHandler, IdentityAlgorithm
from ..infrastructure.providers.User import UserService
from ..utils.DatetimeHandler import checkDatetimeFormat, getDatetime
from ..utils.HandlerError import HandlerError
from ..utils.ResponseHandler import ID_NOT_FOUND, SCHEMA_NOT_MATCH, WRITER_NOT_FOUND


class AuditHandler:
    @staticmethod
    def getFields():
        return ["writeUId", "writeAt", "createUId", "createAt", "endAt"]

    @staticmethod
    def getMock():
        return {
            "writeUId": UserService.getMock(),
            "writeAt": getDatetime(),
            "createUId": UserService.getMock(),
            "createAt": getDatetime(),
            "endAt": getDatetime(),
        }

    def isValid(cls, my_audit: dict) -> list:
        errors = list()

        if my_audit.get("createUId") is None:
            errors.append("Create User is required")

        my_writeAt = my_audit.get("writeAt")
        if my_writeAt is not None:
            if not checkDatetimeFormat(my_writeAt):
                errors.append(SCHEMA_NOT_MATCH)

        my_createAt = my_audit.get("createAt")
        if my_createAt is not None:
            if not checkDatetimeFormat(my_createAt):
                errors.append(SCHEMA_NOT_MATCH)

        my_createAt = my_audit.get("endAt")
        if my_createAt is not None:
            if not checkDatetimeFormat(my_createAt):
                errors.append(SCHEMA_NOT_MATCH)

        return errors

    @classmethod
    def getIdentifier(cls, user_id):
        if not UserService.isValidUserId(user_id):
            raise HandlerError(ID_NOT_FOUND)
        return IdentifierHandler(IdentityAlgorithm.DEFAULT, user_id)

    @classmethod
    def fromDict(cls, params: dict):
        if params.get("writeUId") is None:
            raise HandlerError(WRITER_NOT_FOUND)

        if not UserService.isValidUserId(params.get("writeUId")):
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
        return {"writeUId": current_uid, "writeAt": getDatetime()}

    @classmethod
    def getCreateFields(cls, current_uid):
        if not UserService.isValidUserId(current_uid):
            raise HandlerError(ID_NOT_FOUND)
        return {
            "writeUId": current_uid,
            "writeAt": getDatetime(),
            "createUId": current_uid,
            "createAt": getDatetime(),
            "endAt": None,
        }

    @classmethod
    def getEndFields(cls, current_uid):
        if not UserService.isValidUserId(current_uid):
            raise HandlerError(ID_NOT_FOUND)
        return {
            "writeUId": current_uid,
            "writeAt": getDatetime(),
            "endAt": getDatetime(),
        }
