from typing import Protocol


class ProducerProtocol(Protocol):
    def getToDefaultServer(self):
        pass

    def send_message(self, topic: str, message: str):
        pass
