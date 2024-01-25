from enum import Enum
from typing import Protocol


class BrokerProtocol(Protocol):
    def set_default(self):
        pass

    def send(self, topic: Enum, message: str):
        pass
