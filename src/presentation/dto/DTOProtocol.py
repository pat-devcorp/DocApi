from typing import Protocol, Tuple


class DTOProtocol(Protocol):
    @staticmethod
    def getFields() -> list:
        pass

    @classmethod
    def getSchema(cls):
        pass    

    @staticmethod
    def getMock() -> dict:
        pass

    def asDict(self):
        pass


    @staticmethod
    def getIdentifier(ticketId):
        pass

    @classmethod
    def fromDict(cls, params: dict) -> dict:
        pass
