from enum import Enum


class ProducerTopic(Enum):
    DEFAULT = "default"
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"