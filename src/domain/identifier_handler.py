from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from bson import ObjectId
from sonyflake import SonyFlake

from ..utils.status_code import ID_NOT_VALID
from .DomainError import DomainError


class IdentifierAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1
    USER_ID = 2
    SONYFLAKE = 3
    OBJECT_ID = 4


class IdentifierHandler:
    def __init__(self, algorithm: IdentifierAlgorithm, value):
        self.algorithm = algorithm
        self.value = value

    @classmethod
    def get_default_identifier(cls, algorithm: IdentifierAlgorithm):
        functions = [
            cls.get_string,
            cls.get_uuid_v4,
            cls.get_sonyflake,
            cls.get_object_id,
        ]
        default = functions[algorithm.value]()
        return cls(algorithm, default)

    @staticmethod
    def get_sonyflake():
        sf = SonyFlake()
        return str(sf.next_id())

    @staticmethod
    def get_object_id():
        now = datetime.now()
        return str(ObjectId.from_datetime(now))

    @staticmethod
    def get_string():
        return "DEFAULT"

    @staticmethod
    def get_uuid_v4():
        return str(uuid4())

    @classmethod
    def is_valid(cls, algorithm: IdentifierAlgorithm, identifier) -> None | DomainError:
        if identifier is None:
            raise DomainError(ID_NOT_VALID, "Is Empty")

        validator = [
            cls.is_valid_default,
            cls.is_valid_uuid_v4,
            cls.is_valid_snowflake,
            cls.is_valid_object_id,
        ]
        if not validator[algorithm.value](identifier):
            raise DomainError(ID_NOT_VALID, "Algorithm does not match")
        return cls(algorithm, identifier)

    @staticmethod
    def is_valid_default(identifier):
        return True, ""

    @staticmethod
    def is_valid_snowflake(identifier):
        try:
            sf = SonyFlake()
            sf.parse_id(identifier)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_object_id(identifier):
        try:
            ObjectId(identifier)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_uuid_v4(identifier):
        try:
            UUID(identifier, version=4)
            return True
        except ValueError:
            return False
