# import requests
# from ..config import Config


class UserService:
    @staticmethod
    def isValidUserId(user_id):
        # my_config = Config()
        # payload = {"user_id": user_id}
        # r = requests.get(my_config.USER_API, params=payload)
        # return True if r.status_code == 200 else False
        return True

    @staticmethod
    def getMock():
        return "9999"
