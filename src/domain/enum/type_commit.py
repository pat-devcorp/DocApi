from ..custom_enum import CustomEnum


class TypeCommit(CustomEnum):
    UNDEFINED = 0
    FEAT = 1
    FIX = 2
    BUILD = 3
    CI = 4
    DOCS = 5
    CHORE = 6
    PERFORMANCE = 6
    REFACTOR = 7
    LINTER = 8
    TEST = 9
