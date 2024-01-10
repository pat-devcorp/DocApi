from typing import Protocol

from domain.DomainError import DomainError
from domain.IdentifierHandler import IdentifierHandler
from domain.RepositoryProtocol import RepositoryProtocol
from infrastructure.InfrastructureError import InfrastructureError


class DomainIdentifier(Protocol):
    value: str

    @staticmethod
    def getIdAlgorithm():
        pass

    @classmethod
    def getIdentifier(cls, self):
        pass


class DomainProtocol(Protocol):
    def _asDict() -> dict:
        pass

    def _fields() -> list:
        pass


class DtoProtocol(Protocol):
    @classmethod
    def getMock(cls) -> None:
        pass

    @staticmethod
    def getSchema() -> str:
        pass

    @classmethod
    def isValid(cls, ref_object: dict, is_partial=True) -> tuple[bool, str]:
        pass

    def fromDict(cls, params: dict) -> None | DomainError:
        pass

    def asDict(self) -> dict:
        pass


class DaoProtocol(Protocol):
    @classmethod
    def getMock(cls) -> None:
        pass

    @classmethod
    def getById(cls, ref_repository: RepositoryProtocol, objId: IdentifierHandler):
        pass

    @classmethod
    def delete(cls, writeUId, ref_repository: RepositoryProtocol, objId: IdentifierHandler):
        pass

    @classmethod
    def fromRepository(cls, writeUId, ref_repository: RepositoryProtocol, objId: IdentifierHandler):
        pass

    def toRepository(self) -> dict:
        pass

    def setFields(self, fields: list) -> None:
        pass

    def fetch(self) -> list:
        pass

    def create(self) -> None | InfrastructureError:
        pass

    def update(self) -> None | InfrastructureError:
        pass