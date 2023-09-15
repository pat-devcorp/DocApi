import os


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Config:
    ALLOWED_EXTENSIONS = ["pdf"]
    MAX_FILE_WEIGTH = 16000
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

    def __init__(self):
        self.PROJECT_PATH = os.environ["PROJECT_PATH"]
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.get_config_mongo_database()

    def get_config_mongo_database(self):
        self.MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
        self.MONGO_PORT = os.getenv("MONGO_PORT", 27017)
        self.MONGO_USER = os.getenv("MONGO_USER", "mongo")
        self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "mongo")
        self.MONGO_DATABASE = os.getenv("MONGO_DATABASE", "dev")
