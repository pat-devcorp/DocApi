from enum import Enum
from typing import Protocol


class BrokerProtocol(Protocol):
    def setToDefault(self):
        pass

    def sendMessage(self, topic: Enum, message: str):
        pass
