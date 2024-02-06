from typing import Dict, List

from ..InfrastructureError import InfrastructureError


class MockRepository:
    _name: str
    _pk: str
    _fields: list

    def entity_exists(self, identifier):
        return True

    def fetch(self, fields: list, matching: dict) -> List[Dict[str, any]]:
        return list()

    def get_by_id(self, identifier, fields: list) -> dict:
        return dict()

    def delete(self, identifier) -> None | InfrastructureError:
        return None

    def create(self, data) -> None | InfrastructureError:
        return None

    def update(self, identifier, data) -> None | InfrastructureError:
        return None
