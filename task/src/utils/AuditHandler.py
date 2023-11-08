from collections import namedtuple

from ..infraestructure.middleware.User import validateIdentity
from .DatetimeHandler import getDatetime, valdiateDatetimeFormat
from .HandlerError import HandlerError
from .IdentityHandler import IdentityAlgorithm, IdentityHandler

AuditDTO = namedtuple("audit", ["write_uid", "write_at", "create_uid", "create_at"])


class AuditHandler:
    def _validate(cls, my_audit: dict) -> list:
        errors = list()

        if my_audit.get("create_uid") is None:
            errors.append("Create User is required")

        my_write_at = my_audit.get("write_at")
        if my_write_at is not None:
            if not valdiateDatetimeFormat(my_write_at):
                errors.append("Date format is not supported for write datetime")

        my_create_at = my_audit.get("create_at")
        if my_create_at is not None:
            if not valdiateDatetimeFormat(my_create_at):
                errors.append("Date format is not supported for create datetime")

        return errors

    @classmethod
    def getIdentifier(cls, user_id):
        if not validateIdentity(user_id):
            raise HandlerError("User ID is not valid")
        return IdentityHandler(IdentityAlgorithm.DEFAULT, user_id)

    @classmethod
    def fromDict(cls, params: dict):
        if params.get("write_uid") is None:
            raise HandlerError("User for write is required")

        audit_dto = dict()
        for k in AuditDTO._fields:
            audit_dto[k] = params[k] if params.get(k) is not None else None

        errors = cls._validate(params)
        if len(errors) > 0:
            raise HandlerError("\n".join(errors))

        return AuditDTO(**audit_dto)

    @classmethod
    def getUpdateFields(cls, current_uid):
        return {"write_uid": current_uid, "write_at": getDatetime()}

    @classmethod
    def getNewAudit(cls, current_uid):
        return AuditDTO(
            write_uid=current_uid,
            write_at=getDatetime(),
            create_uid=current_uid,
            create_at=getDatetime(),
        )
