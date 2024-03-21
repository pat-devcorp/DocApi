from enum import Enum
from uuid import UUID, uuid4

from ..utils.response_code import ID_NOT_VALID
from .DomainError import DomainError


class IdentifierAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1
    USER_ID = 2


class IdentifierHandler:
    def __init__(self, pk: str, algorithm: IdentifierAlgorithm) -> None:
        self.pk = pk
        self.algorithm = algorithm

    def get_default_identifier(self):
        default = [
            self.get_string,
            self.get_uuid_v4,
        ]
        return default[self.algorithm.value]()

    @staticmethod
    def get_string():
        return "DEFAULT"

    @staticmethod
    def get_uuid_v4():
        return str(uuid4())

    def is_valid(self, identifier) -> None | DomainError:
        validator = [self.is_valid_default, self.is_valid_uuid_v4]
        is_ok, err = validator[self.algorithm.value](identifier)
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
