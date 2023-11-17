import re
from enum import Enum

from ..infraestructure.UserValidator import UserValidator
from ..utils.ErrorHandler import ID_NOT_VALID


class IdentityAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1
    USER_ID = 2


class IdentifierHandler:
    value = None

    def __init__(self, algorithm: IdentityAlgorithm):
        self.algorithm = algorithm

    def setIdentifier(self, identifier):
        is_ok, err = self.isValid(identifier, self.algorithm)
        if not is_ok:
            raise ValueError(ID_NOT_VALID, err)
        self.value = identifier

    @classmethod
    def isValid(cls, identifier, algorithm: IdentityAlgorithm) -> tuple[bool, str]:
        identifier_functions = [cls.ensureDefault, cls.ensureUuidV4, cls.ensureUserId]
        return identifier_functions[algorithm.value](identifier)

    @staticmethod
    def ensureDefault(identifier):
        return True, ""

    @staticmethod
    def ensureUuidV4(identifier) -> tuple[bool, str]:
        if identifier is None or len(identifier) == 0:
            return False, "Is Empty"

        uuid_v4_pattern = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if not bool(uuid_v4_pattern.match(identifier)):
            return False, "Algorithm doesnt match"
        return True, ""

    @staticmethod
    def ensureUserId(identifier) -> tuple[bool, str]:
        if not UserValidator.isValidUserID(identifier):
            return False, "User doesnt exists"
        return True, ""

    def __str__(self):
        return str(self.value)
