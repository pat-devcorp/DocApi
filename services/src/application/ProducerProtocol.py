from typing import Protocol


class ProducerProtocol(Protocol):
    def setToDefault(self):
        pass

    def sendMessage(self, topic: str, message: str):
        pass
