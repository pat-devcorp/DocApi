import requests
from pydantic import BaseModel

from ...domain.enum.identifier_algorithm import IdentifierAlgorithm
from ...domain.identifier_handler import IdentifierHandler


class UserService:
    _algorithm = IdentifierAlgorithm.UUID_V4
    _pk = "userId"

    def __init__(self, userServiceUrl: str) -> None:
        self.userClient = ref_user_service

    def is_valid_user_id(self, userId) -> bool:
        payload = {self._pk: userId}
        r = requests.get(self.userClient.url, params=payload)
        return True if r.status_code == 200 else False

    @classmethod
    def get_default_identifier(cls) -> IdentifierHandler:
        return IdentifierHandler.get_default_identifier(cls._algorithm)

    @classmethod
    def set_identifier(cls, identifier) -> IdentifierHandler:
        return IdentifierHandler.is_valid(cls._algorithm, identifier)
