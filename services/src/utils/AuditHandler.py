from collections import namedtuple

from .DatetimeHandler import DateTimeHandler
from .HandlerError import HandlerError

AuditStruct = namedtuple("audit", ["write_uid", "write_at", "create_uid", "create_at"])


class AuditHandler:
    @classmethod
    def validate(cls, my_audit: dict) -> AuditStruct:
        errors = list()

        my_write_at = my_audit.get("write_at")
        if my_write_at is not None:
            if not DateTimeHandler.valdiateDatetimeFormat(my_write_at):
                errors.append("Date format is not supported for write datetime")

        my_create_at = my_audit.get("create_at")
        if my_create_at is not None:
            if not DateTimeHandler.valdiateDatetimeFormat(my_create_at):
                errors.append("Date format is not supported for create datetime")

        if len(errors) > 0:
            raise HandlerError("\n".join(errors))

        return AuditStruct(**my_audit)

    @classmethod
    def fromDict(cls, params: dict):
        if params.get("write_uid") is None:
            raise HandlerError("User for write is required")

        my_audit = {k: v for k, v in params.items() if k in AuditStruct._fields}
        cls.create(**my_audit)

    @classmethod
    def create(cls, write_uid, create_uid=None, create_at=None, write_at=None):
        now = DateTimeHandler.getDatetime()
        my_audit = {
            "write_uid": write_uid,
            "write_at": (write_at or now),
            "create_uid": (create_uid or write_uid),
            "create_at": (create_at or now),
        }
        return cls.validate(my_audit)

    @classmethod
    def update(cls, current_uid, old_audit: dict):
        errors = list()

        if old_audit.get("create_uid") is None:
            errors.append("User that create the entity is not defined")

        if old_audit.get("create_at") is None:
            errors.append("The date that entity was created is not defined")

        if len(errors) > 0:
            raise HandlerError("\n".join(errors))

        cls.create(current_uid, old_audit["create_uid"], old_audit["create_at"])

    @classmethod
    def getUpdateFields(cls, current_uid):
        return {"write_uid": current_uid, "write_at": DateTimeHandler.getDatetime()}
