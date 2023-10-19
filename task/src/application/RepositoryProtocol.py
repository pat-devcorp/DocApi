from collections import namedtuple
from enum import Enum
from typing import Dict, List, Protocol


class RepositoryProtocol(Protocol):
    def setToDefault(cls):
        pass
    
    def stateMachine(self, state: Enum, event: Enum) -> dict:
        pass

    def ensureEntity(self, my_object: namedtuple) -> bool:
        return True

    def get(self, tablename: str, attrs: List[str]) -> List[Dict]:
        pass

    def getByID(self, tablename: str, pk: str, id_val: str, attrs: List[str]) -> Dict:
        pass

    def update(self, tablename: str, pk: str, id_val: str, kwargs: dict):
        pass

    def create(self, tablename: str, kwargs: dict):
        pass
