from collections import namedtuple

from ..domain.DomainError import DomainError
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
            raise DomainError(errors)

        return AuditStruct(**my_audit)

    @classmethod
    def fromDict(cls, params: dict):
        if params.get("write_uid") is None:
            raise HandlerError("User for write is required")
        my_audit = {k: v for k, v in params.items() if k in AuditStruct._fields}
        cls.create(**my_audit)

    @classmethod
    def create(
        cls, write_uid, create_uid=None, create_at: str = None, write_at: str = None
    ):
        now = DateTimeHandler.getDatetime()
        my_audit = {
            "write_uid": write_uid,
            "create_uid": (create_uid or write_uid),
            "create_at": (create_at or now),
            "write_at": (write_at or now),
        }
        return cls.validate(my_audit)

    @classmethod
    def update(cls, write_uid, ref_audit: AuditStruct):
        my_audit = {
            "write_uid": write_uid,
            "create_uid": ref_audit.create_uid,
            "create_at": ref_audit.create_at,
        }
        return cls.validate(my_audit)
