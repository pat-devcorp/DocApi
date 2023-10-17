from enum import Enum
from typing import Protocol


class ProducerTopic(Enum):
    DEFAULT = "default"
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"


class ProducerProtocol(Protocol):
    def setToDefault(self):
        pass

    def sendMessage(self, topic: str, message: str):
        pass
