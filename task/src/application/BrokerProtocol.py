from typing import Protocol

from .BrokerTopic import BrokerTopic

class BrokerProtocol(Protocol):
    def setToDefault(self):
        pass

    def sendMessage(self, topic: BrokerTopic, message: str):
        pass
