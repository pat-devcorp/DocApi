# import requests
# from ..config import Config


from collections import namedtuple

from ...domain.identifier_handler import IdentityAlgorithm
from ..InfrastructureError import InfrastructureError

UserIdentifier = namedtuple("UserIdentifier", "value")


class UserService:
    @staticmethod
    def is_valid_user_id(userUId):
        # my_config = Config()
        # payload = {"user_id": user_id}
        # r = requests.get(my_config.USER_API, params=payload)
        # return True if r.status_code == 200 else False
        return True

    @classmethod
    def set_identifier(cls, userUId) -> UserIdentifier | InfrastructureError:
        if not cls.is_valid_user_id(userUId):
            raise InfrastructureError("Invalid user_id: %s" % userUId)
        return UserIdentifier(userUId, "userId", IdentityAlgorithm.DEFAULT)

    @staticmethod
    def get_mock():
        return "87378b40-894c-11ee-b9d1-0242ac120002"

    @staticmethod
    def test_user_service(userUId):
        pass
