from typing import Protocol, Tuple


class DAOProtocol(Protocol):
    def asDict(self) -> dict:
        pass

    @staticmethod
    def getIdAlgorithm():
        pass
    
    @staticmethod
    def getSchema():
        pass
    
    @staticmethod
    def getFields() -> list:
        pass

    @staticmethod
    def getMock() -> dict:
        pass


    @classmethod
    def isValid(cls, ref_object: dict, is_partial=True) -> Tuple[bool, str]:
        pass

    def updatedObj():
        pass
    

class DomainProtocol(Protocol):
    def setFields(self, fields: list):
        pass
    
    def prepareIdentity(self, identifier) -> IdentityHandler | DomainError:
        pass

    def fetch(self) -> list:
        pass

    
    def doGetByID(self, daoId: IdentityHandler) -> list:
        pass
    
    def doDelete(self, daoId: IdentityHandler) -> bool:
        pass
    
    def doCreate(self, dao: DAOProtocol) -> bool:
        pass
    
    def doUpdate(self, dao: DAOProtocol) -> bool:
        pass