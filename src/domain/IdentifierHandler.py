from enum import Enum
from uuid import UUID, uuid4

from ..infrastructure.providers.User import UserService
from ..utils.ResponseHandler import ID_NOT_VALID


class IdentityAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1
    USER_ID = 2


class IdentifierHandler:
    value = None

    def __init__(self, algorithm: IdentityAlgorithm):
        self.algorithm = algorithm

    def setIdentifier(self, identifier) -> None | ValueError:
        is_ok, err = self.isValid(identifier, self.algorithm)
        if not is_ok:
            raise ValueError(ID_NOT_VALID, err)
        self.value = identifier

    def getIdentifier(self):
        identifier_functions = [self.getDefault, self.getUuidV4, self.getDefault]
        self.value = identifier_functions[self.algorithm]()

    @staticmethod
    def getDefault():
        return "DEFAULT"

    @staticmethod
    def getUuidV4():
        return uuid4()

    @classmethod
    def isValid(cls, identifier, algorithm: IdentityAlgorithm) -> tuple[bool, str]:
        identifier_functions = [
            cls.isValidDefault,
            cls.isValidUuidV4,
            cls.isValidUserId,
        ]
        return identifier_functions[algorithm.value](identifier)

    @staticmethod
    def isValidDefault(identifier):
        return True, ""

    @staticmethod
    def isValidUuidV4(identifier) -> tuple[bool, str]:
        if identifier is None or len(identifier) == 0:
            return False, "Is Empty"

        try:
            uuid_obj = UUID(identifier, version=4)
            return True, uuid_obj
        except ValueError:
            return False, "Algorithm does not match"

    @staticmethod
    def isValidUserId(identifier) -> tuple[bool, str]:
        if not UserService.isValidUserId(identifier):
            return False, "User does not exists"
        return True, ""

    def __str__(self):
        return str(self.value)
