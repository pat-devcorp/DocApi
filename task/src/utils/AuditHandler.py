from collections import namedtuple

from ..infraestructure.middleware.User import isValidUserID
from ..utils.ErrorHandler import FORMAT_NOT_MATCH, ID_NOT_FOUND, WRITE_UID_NOT_FOUND
from .DatetimeHandler import getDatetime, valdiateDatetimeFormat
from .HandlerError import HandlerError
from .IdentityHandler import IdentityAlgorithm, IdentityHandler

AuditDTO = namedtuple("audit", ["write_uid", "write_at", "create_uid", "create_at"])


class AuditHandler:
    def isValid(cls, my_audit: dict) -> list:
        errors = list()

        if my_audit.get("create_uid") is None:
            errors.append("Create User is required")

        my_write_at = my_audit.get("write_at")
        if my_write_at is not None:
            if not valdiateDatetimeFormat(my_write_at):
                errors.append(FORMAT_NOT_MATCH)

        my_create_at = my_audit.get("create_at")
        if my_create_at is not None:
            if not valdiateDatetimeFormat(my_create_at):
                errors.append(FORMAT_NOT_MATCH)

        return errors

    @classmethod
    def getIdentifier(cls, user_id):
        if not isValidUserID(user_id):
            raise HandlerError(ID_NOT_FOUND)
        return IdentityHandler(IdentityAlgorithm.DEFAULT, user_id)

    @classmethod
    def fromDict(cls, params: dict):
        if params.get("write_uid") is None:
            raise HandlerError(WRITE_UID_NOT_FOUND)
        
        if not isValidUserID(params.get("write_uid")):
            raise HandlerError(ID_NOT_FOUND)

        audit_dto = dict()
        for k in AuditDTO._fields:
            audit_dto[k] = params[k] if params.get(k) is not None else None

        errors = cls.isValid(params)
        if len(errors) > 0:
            raise HandlerError("\n".join(errors))

        return AuditDTO(**audit_dto)

    @classmethod
    def getUpdateFields(cls, current_uid):
        return {"write_uid": current_uid, "write_at": getDatetime()}

    @classmethod
    def create(cls, current_uid):
        if not isValidUserID(current_uid):
            raise HandlerError(ID_NOT_FOUND)
        
        return AuditDTO(
            write_uid=current_uid,
            write_at=getDatetime(),
            create_uid=current_uid,
            create_at=getDatetime(),
        )
