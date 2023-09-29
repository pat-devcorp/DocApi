from collections import namedtuple
from datetime import datetime
import re


AuditStruct = namedtuple('AuditStruct', [
        "audit_id",
        "write_uid",
        "write_at",
        "create_uid",
        "create_at",
        "is_active"
    ])

class Audit:
    audit_id: str
    is_active: bool
    write_uid: str
    create_uid: str
    write_at: str
    create_at: str


    @staticmethod
    def validate(input_dict: dict):
        errors = list()
        id_errors = Audit.ensureUuidV4(input_dict.get("audit_id"))
        if len(id_errors) > 0:
            errors.append(id_errors)
        write_uid_errors = Audit.ensureUserID(input_dict.get("write_uid"))
        if len(write_uid_errors) > 0:
            errors.append(write_uid_errors)
        return errors

    @staticmethod
    def ensureDateFormat(write_at):
        try:
            datetime.strftime(write_at, "%d/%m/%Y, %H:%M:%S")
            return ''
        except ValueError:
            return "Date format is not supported"

    @staticmethod
    def ensureUuidV4(identity: str):
        if identity is None or len(identity) == 0:
            return "\nEmpty description"
        
        uuid_v4_pattern = re.compile(
            r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
        )
        if not bool(uuid_v4_pattern.match(identity)):
            return "\nIs not a valid identity"
        return ''
    
    @staticmethod
    def ensureUserID(write_uid):
        if write_uid is not None:
            return "User identity is not defined"
        return ''

    @classmethod
    def fromDict(cls, params: dict):
        my_audit = {k: v for k, v in params.items() if k in AuditStruct._fields}
        
        cls.create(**my_audit)

    @classmethod
    def create(
        self,
        audit_id,
        write_uid,
        create_uid=None,
        is_active=True,
        write_at=None,
        create_at=None,
    ) -> AuditStruct:
        now = datetime.strftime(datetime.now(), "%d/%m/%Y, %H:%M:%S")
        my_audit = {
            "audit_id": audit_id,
            'write_uid': write_uid,
            'create_uid': (create_uid or write_uid),
            'is_active': is_active,
            'write_at': (write_at or now),
            'create_at': (create_at or now)
        }
        self.validate(my_audit)
        return AuditStruct(**my_audit)
