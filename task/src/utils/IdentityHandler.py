import re
from enum import Enum

from ..infraestructure.middleware.User import isValidUserID

from ..utils.ErrorHandler import ID_NOT_FOUND, ID_NOT_VALID
from ..utils.HandlerError import HandlerError


class IdentityAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1
    USER_ID = 2


class IdentityHandler:
    value = None

    def __init__(self, algorithm: IdentityAlgorithm, identifier):
        self.algorithm = algorithm
        self.value = identifier

    @classmethod
    def isValid(cls, identifier, algorithm: IdentityAlgorithm) -> bool:
        identifier_functions = [cls.ensureDefault, cls.ensureUuidV4, cls.ensureUserId]
        error = identifier_functions[algorithm.value](identifier)
        if len(error) > 0:
            return False
        return True

    @staticmethod
    def ensureDefault(identifier):
        return ""

    @staticmethod
    def ensureUuidV4(identifier) -> str:
        if identifier is None or len(identifier) == 0:
            return ID_NOT_FOUND

        uuid_v4_pattern = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if not bool(uuid_v4_pattern.match(identifier)):
            return ID_NOT_VALID
        return ""

    @staticmethod
    def ensureUserId(identifier):
        if not isValidUserID(identifier):
            return ID_NOT_FOUND
        return ""

    def __str__(self):
        return str(self.value)
