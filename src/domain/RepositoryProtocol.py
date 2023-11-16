from typing import Dict, List, Protocol


class RepositoryProtocol(Protocol):
    def entityExists(self, identifier):
        pass

    def fetch(self, tablename: str, attrs: List[str]) -> List[Dict]:
        pass

    def create(self, tablename: str, params: dict):
        pass

    def update(self, tablename: str, pk: str, identifier: str, params: dict):
        pass

    def getByID(
        self, tablename: str, pk: str, identifier: str, attrs: List[str]
    ) -> Dict:
        pass

    def delete(self, tablename: str, pk: str, identifier: str):
        pass
