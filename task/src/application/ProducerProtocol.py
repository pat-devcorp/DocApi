from typing import Protocol

from .ProducerTopic import ProducerTopic

class ProducerProtocol(Protocol):
    def setToDefault(self):
        pass

    def sendMessage(self, topic: ProducerTopic, message: str):
        pass
