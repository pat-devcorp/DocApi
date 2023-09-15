from typing import Dict, List, Protocol


class RepositoryProtocol(Protocol):
    def get(self, tablename: str, attrs: List[str]) -> List[Dict]:
        pass

    def get_by_id(self, tablename: str, pk: str, id_val: str, attrs: List[str]) -> Dict:
        pass

    def update(self, tablename: str, pk: str, id_val: str, kwargs: dict):
        pass

    def create(self, tablename: str, kwargs: dict):
        pass
