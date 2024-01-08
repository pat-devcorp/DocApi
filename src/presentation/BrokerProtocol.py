from typing import Protocol

from ..application.BrokerTopic import BrokerTopic


class BrokerProtocol(Protocol):
    def setToDefault(self):
        pass

    def sendMessage(self, topic: BrokerTopic, message: str):
        pass
