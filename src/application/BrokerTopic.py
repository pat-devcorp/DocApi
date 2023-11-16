from enum import Enum


class BrokerTopic(Enum):
    DEFAULT = "default"
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
