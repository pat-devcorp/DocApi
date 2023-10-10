import re
from enum import Enum


class IdentityAlgorithm(Enum):
    DEFAULT = 0
    UUID_V4 = 1


class IdentityHandler:
    _id = None

    def __init__(self, algorithm: IdentityAlgorithm):
        self.algorithm = algorithm

    def setIdentity(self, identity):
        self.validateIdentity(identity, self.algorithm)
        self._id = identity

    @classmethod
    def validate(cls, identity, algorithm: IdentityAlgorithm) -> bool:
        identity_functions = [cls.ensureDefault, cls.ensureUuidV4]
        error_identity = identity_functions[algorithm.value](identity)
        if len(error_identity) > 0:
            raise ValueError(error_identity)
        return True

    @staticmethod
    def ensureDefault(identity):
        return ""

    @staticmethod
    def ensureUuidV4(identity: str):
        if identity is None or len(identity) == 0:
            return "\nEmpty identifier"

        uuid_v4_pattern = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
        )
        if not bool(uuid_v4_pattern.match(identity)):
            return "\nIs not a valid identity"
        return ""

    def __str__(self):
        return str(self._id)
