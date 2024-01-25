# import requests
# from ..config import Config


class UserService:
    @staticmethod
    def is_valid_user_id(userUId):
        # my_config = Config()
        # payload = {"user_id": user_id}
        # r = requests.get(my_config.USER_API, params=payload)
        # return True if r.status_code == 200 else False
        return True


def get_mock():
    return "87378b40-894c-11ee-b9d1-0242ac120002"


def test_user_service(userUId):
    pass
