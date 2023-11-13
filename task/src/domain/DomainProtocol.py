from typing import Protocol


class DomainProtocol(Protocol):
    @staticmethod
    def getFields() -> list:
        pass

    @staticmethod
    def getMock() -> dict:
        pass
    
    @staticmethod
    def create(**kwargs) -> dict:
        pass

    @classmethod
    def fromDict(cls, params: dict) -> dict:
        pass

    @classmethod
    def isValid(cls, ref_object: dict, is_partial=True) -> Tuple[bool, str]:
        pass