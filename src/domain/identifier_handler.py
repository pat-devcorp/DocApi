from datetime import datetime
from uuid import UUID, uuid4

from bson import ObjectId
from nanoid import generate
from sonyflake import SonyFlake

from ..utils.status_code import ID_NOT_VALID
from .DomainError import DomainError
from .enum.identifier_algorithm import IdentifierAlgorithm


class IdentifierHandler:
    def __init__(self, algorithm: IdentifierAlgorithm, value):
        self.algorithm = algorithm
        self.value = value

    @classmethod
    def get_default_identifier(cls, algorithm: IdentifierAlgorithm):
        functions = [
            cls.get_default,
            cls.get_uuid_v4,
            cls.get_sony_flake,
            cls.get_object_id,
            cls.get_nanoid,
        ]
        default = functions[algorithm.value]()
        return cls(algorithm, default)

    @staticmethod
    def get_sony_flake():
        sf = SonyFlake()
        return str(sf.next_id())

    @staticmethod
    def get_object_id():
        now = datetime.now()
        return str(ObjectId.from_datetime(now))

    @staticmethod
    def get_nanoid():
        return generate()

    @staticmethod
    def get_default():
        return "N/A"

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
            cls.is_valid_nano_id,
        ]
        if not validator[algorithm.value](identifier):
            raise DomainError(ID_NOT_VALID, "Algorithm does not match")
        return cls(algorithm, identifier)

    @staticmethod
    def is_valid_default(identifier):
        return True

    @staticmethod
    def is_valid_snowflake(identifier: str):
        if not isinstance(identifier, str):
            return False
        if len(identifier) != 18:
            return False
        return True

    @staticmethod
    def is_valid_object_id(identifier):
        try:
            ObjectId(identifier)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_nano_id(identifier: str):
        if not isinstance(identifier, str):
            return False
        if len(identifier) != 21:
            return False
        return True

    @staticmethod
    def is_valid_uuid_v4(identifier):
        if not isinstance(identifier, str):
            return False
        try:
            UUID(identifier, version=4)
            return True
        except ValueError:
            return False
