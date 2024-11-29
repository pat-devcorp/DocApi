from datetime import datetime
from uuid import UUID, uuid4

from bson import ObjectId
from nanoid import generate
from sonyflake import SonyFlake

from .domain_error import DomainError
from .enum.identifier_algorithm import IdentifierAlgorithm
from .model.constant import ID_NOT_VALID


class IdentifierHandler:
    def __init__(self, algorithm: IdentifierAlgorithm):
        self._algorithm = algorithm

    def get_default_identifier(self, algorithm: IdentifierAlgorithm):
        functions = [
            self.get_default,
            self.get_uuid_v4,
            self.get_sony_flake,
            self.get_object_id,
            self.get_nanoid,
        ]
        return functions[algorithm.value]()

    @staticmethod
    def get_sony_flake() -> str:
        sf = SonyFlake()
        return str(sf.next_id())

    @staticmethod
    def get_object_id() -> str:
        now = datetime.now()
        return str(ObjectId.from_datetime(now))

    @staticmethod
    def get_nanoid() -> str:
        return generate()

    @staticmethod
    def get_default() -> str:
        return "N/A"

    @staticmethod
    def get_uuid_v4() -> str:
        return str(uuid4())

    def is_valid(self, identifier) -> bool:
        if identifier is None:
            return False

        validator = [
            self.is_valid_default,
            self.is_valid_uuid_v4,
            self.is_valid_snowflake,
            self.is_valid_object_id,
            self.is_valid_nano_id,
        ]
        return validator[self._algorithm](identifier)

    @staticmethod
    def is_valid_default(identifier) -> bool:
        return True

    @staticmethod
    def is_valid_snowflake(identifier: str) -> bool:
        if not isinstance(identifier, str):
            return False
        if len(identifier) != 18:
            return False
        return True

    @staticmethod
    def is_valid_object_id(identifier) -> bool:
        try:
            ObjectId(identifier)
            return True
        except ValueError:
            return False

    @staticmethod
    def is_valid_nano_id(identifier: str) -> bool:
        if not isinstance(identifier, str):
            return False
        if len(identifier) != 21:
            return False
        return True

    @staticmethod
    def is_valid_uuid_v4(identifier) -> bool:
        if not isinstance(identifier, str):
            return False
        try:
            UUID(identifier, version=4)
            return True
        except ValueError:
            return False
