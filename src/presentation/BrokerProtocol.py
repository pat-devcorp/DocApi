from enum import Enum
from typing import Protocol


class BrokerProtocol(Protocol):
    def setDefault(self):
        pass

    def send(self, topic: Enum, message: str):
        pass
