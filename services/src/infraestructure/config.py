import os

from ..utils.singleton import singleton


@singleton
class Config:
    def __init__(self):
        current_directory = os.getcwd()
        self.PROJECT_PATH = os.path.abspath(os.path.join(current_directory, "..", ".."))
        self.SECRET_KEY = os.getenv("SECRET_KEY", "BatmanisBruceWayne")
        self.API_VERSION = os.getenv("API_VERSION", "1.0.0")

        allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "pdf")
        self.ALLOWED_EXTENSIONS = allowed_extensions.split(",")
        self.MAX_FILE_WEIGTH = os.getenv("MAX_FILE_WEIGTH", 16000)
        self.DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d")
        self.TIME_FORMAT = os.getenv("TIME_FORMAT", "%H:%M:%S")
        self.DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")

        self.PRODUCER_HOST = os.getenv("PRODUCER_HOST", "172.25.0.2")
        self.PRODUCER_PORT = os.getenv("PRODUCER_PORT", 9092)

        self.MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
        self.MONGO_PORT = os.getenv("MONGO_PORT", 27017)
        self.MONGO_USER = os.getenv("MONGO_USER", "mongo")
        self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "mongo")
        self.MONGO_DATABASE = os.getenv("MONGO_DATABASE", "dev")
