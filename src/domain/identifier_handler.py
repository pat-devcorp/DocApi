from enum import Enum
from uuid import UUID, uuid4

from ..utils.response_code import ID_NOT_VALID
from .DomainError import DomainError


class IdentifierAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1
    USER_ID = 2


class IdentifierHandler:
    @classmethod
    def get_default_identifier(cls, algorithm: IdentifierAlgorithm):
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
    def is_valid(cls, algorithm: IdentifierAlgorithm, identifier) -> None | DomainError:
        validator = [cls.is_valid_default, cls.is_valid_uuid_v4]
        is_ok, err = validator[algorithm.value](identifier)
        if not is_ok:
            raise DomainError(ID_NOT_VALID, err)

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
