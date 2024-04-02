import requests
from pydantic import BaseModel

from ...domain.identifier_handler import IdentifierAlgorithm, IdentifierHandler


class UserServer(BaseModel):
    url: str


class UserService:
    algorithm = IdentifierAlgorithm.UUID_V4
    pk = "user_id"

    def __init__(self, ref_user_service: UserServer):
        self.user_client = ref_user_service

    def is_valid_user_id(self, user_id):
        payload = {"user_id": user_id}
        r = requests.get(self.user_client.url, params=payload)
        return True if r.status_code == 200 else False

    @classmethod
    def get_default_identifier(cls):
        return IdentifierHandler.get_default_identifier(cls.algorithm)

    @classmethod
    def set_identifier(cls, identifier):
        return IdentifierHandler.is_valid(cls.algorithm, identifier)
