from datetime import datetime
from uuid import uuid4

from ..infraestructure.config import Config


class AuditId:
    def __init__(self, value=None):
        self._id = value

    def __str__(self):
        return self._id

    @classmethod
    def get_new_id(cls):
        return cls(str(uuid4()))


class Audit:
    _id: AuditId
    is_active: bool
    create_at: datetime
    write_at: datetime

    __tablename__ = "audit"
    __fields__ = [
        "_id",
        "create_uid",
        "write_uid",
        "is_active",
        "create_at",
        "write_at",
    ]

    write_uid = None
    create_uid = None

    @staticmethod
    def validate_schema(input_dict: dict):
        errors = dict()
        error_write_uid = Audit.ensure_write_uid(input_dict.get("write_uid"))
        if error_write_uid is not None:
            errors.update(error_write_uid)
        return errors

    @staticmethod
    def ensure_write_uid(write_uid):
        if write_uid is not None:
            return {"write_uid": "Not allowed"}
        return None

    @classmethod
    def from_dict(cls, params: dict):
        df = {k: v for k, v in params.items() if k in cls.__fields__}
        identity = df.get("_id")
        if identity is not None:
            df._id = AuditId(df._id)
        return cls(**df)

    def as_dict(self):
        my_config = Config()
        return {
            "_id": str(self._id),
            "is_active": self.is_active,
            "write_uid": self.write_uid,
            "write_at": datetime.strftime(self.write_at, my_config.DATETIME_FORMAT),
            "create_uid": self.create_uid,
            "create_at": datetime.strftime(self.create_at, my_config.DATETIME_FORMAT),
        }

    def __init__(
        self,
        write_uid,
        create_uid=None,
        is_active=True,
        create_at=datetime.now(),
        write_at=None,
        _id=None,
    ):
        self.write_uid = write_uid
        self.create_uid = (create_uid or write_uid)
        self.is_active = is_active
        self.create_at = create_at
        self.write_at = (write_at or create_at)
        self._id = (_id or AuditId.get_new_id())

    def update(self, write_uid):
        self.write_uid = write_uid
        self.write_at = datetime.now()

    def deactivate(self, write_uid):
        self.is_active = False
        self.update(write_uid)
