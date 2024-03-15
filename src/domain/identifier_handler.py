from enum import Enum
from uuid import UUID, uuid4

from ..infrastructure.services.User import UserService


class IdentityAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1
    USER_ID = 2


class IdentifierHandler:
    def __init__(self, algorithm: IdentityAlgorithm):
        self.algorithm = algorithm

    @classmethod
    def get_default(cls, algorithm: IdentityAlgorithm):
        default = [
            cls.get_string,
            cls.get_uuid_v4,
        ]
        return default[algorithm.value]()

    @staticmethod
    def get_string():
        return "DEFAULT"

    @staticmethod
    def get_uuid_v4():
        return str(uuid4())

    @classmethod
    def is_valid(cls, identifier, algorithm: IdentityAlgorithm) -> tuple[bool, str]:
        validator = [
            cls.is_valid_default,
            cls.is_valid_uuid_v4,
            cls.is_valid_user_id,
        ]
        return validator[algorithm.value](identifier)

    @staticmethod
    def is_valid_default(identifier):
        return True, ""

    @staticmethod
    def is_valid_uuid_v4(identifier) -> tuple[bool, str]:
        if identifier is None or len(identifier) == 0:
            return False, "Is Empty"

        try:
            UUID(identifier, version=4)
            return True, ""
        except ValueError:
            return False, "Algorithm does not match"

    @staticmethod
    def is_valid_user_id(identifier) -> tuple[bool, str]:
        if not UserService.is_valid_user_id(identifier):
            return False, "User does not exists"
        return True, ""
