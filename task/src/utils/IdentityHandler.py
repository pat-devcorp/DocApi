import re
from enum import Enum

from ..utils.ErrorHandler import ID_NOT_FOUND, ID_NOT_VALID
from ..utils.HandlerError import HandlerError


class IdentityAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1


class IdentityHandler:
    _id = None

    def __init__(self, algorithm: IdentityAlgorithm, identity):
        self.algorithm = algorithm
        self._id = identity

    @classmethod
    def validate(cls, identity, algorithm: IdentityAlgorithm) -> bool:
        identity_functions = [cls.ensureDefault, cls.ensureUuidV4]
        error = identity_functions[algorithm.value](identity)
        if len(error) > 0:
            return False
        return True

    @staticmethod
    def ensureDefault(identity):
        return ""

    @staticmethod
    def ensureUuidV4(identity) -> str:
        if identity is None or len(identity) == 0:
            return ID_NOT_FOUND

        uuid_v4_pattern = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if not bool(uuid_v4_pattern.match(identity)):
            return ID_NOT_VALID
        return ""

    def __str__(self):
        return str(self._id)
