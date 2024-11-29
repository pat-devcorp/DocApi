from ..custom_enum import CustomEnum


class TaskState(CustomEnum):
    CREATED = 0
    DELETED = 1
    IN_PROCESS = 2
    OBSERVE = 3
    END = 4
