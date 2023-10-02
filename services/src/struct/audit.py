from collections import namedtuple

from .DomainError import DomainError
from .utils.datetime import ensureDatetimeFormat, getDatetime
from .utils.identity import Identity, IdentityAlgorithm

AuditStruct = namedtuple("audit", ["write_uid", "write_at", "create_uid", "create_at"])


class Audit:
    @staticmethod
    def validate(my_audit: dict) -> AuditStruct:
        errors = list()

        my_write_at = my_audit.get("write_at")
        if my_write_at is not None:
            if not ensureDatetimeFormat(my_write_at):
                errors.append("Date format is not supported for write datetime")

        my_create_at = my_audit.get("create_at")
        if my_create_at is not None:
            if not ensureDatetimeFormat(my_create_at):
                errors.append("Date format is not supported for create datetime")

        if len(errors) > 0:
            raise DomainError(errors)

        return AuditStruct(**my_audit)

    @classmethod
    def fromDict(cls, params: dict):
        my_audit = {k: v for k, v in params.items() if k in AuditStruct._fields}

        cls.create(**my_audit)

    @classmethod
    def create(
        self,
        write_uid: Identity(IdentityAlgorithm(0)),
        create_uid: Identity(IdentityAlgorithm(0)),
        write_at: str = None,
        create_at: str = None,
    ) -> AuditStruct:
        now = getDatetime()
        my_audit = {
            "write_uid": write_uid,
            "create_uid": (create_uid or write_uid),
            "write_at": (write_at or now),
            "create_at": (create_at or now),
        }
        return self.validate(my_audit)

    @classmethod
    def udpate(cls, write_uid, my_audit: AuditStruct):
        my_audit.write_uid = write_uid
        my_audit.write_at = getDatetime()
        return cls.validate(my_audit)
