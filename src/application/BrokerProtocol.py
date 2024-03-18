from enum import Enum
from typing import Protocol


class BrokerProtocol(Protocol):
    def publish(self, topic: Enum, message: str):
        pass
