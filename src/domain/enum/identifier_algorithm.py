from ..custom_enum import CustomEnum


class IdentifierAlgorithm(CustomEnum):
    DEFAULT = 0
    UUID_V4 = 1
    SONY_FLAKE = 2
    OBJECT_ID = 3
    NANO_ID = 4
