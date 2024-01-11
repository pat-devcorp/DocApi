import os

from .singleton import singleton


@singleton
class Config:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_PATH = os.path.abspath(os.path.join(current_directory, ".."))
        self.ROUTE_PATH = "src/web/route"
        self.LOG_PATH = "src/log/api.log"
        self.SECRET_KEY = os.getenv("SECRET_KEY", "BatmanIsBruceWayne")
        self.API_VERSION = os.getenv("API_VERSION", "1.0.0.0")
        self.IS_IN_PRODUCTION = os.getenv("IS_IN_PRODUCTION", 0)
        self.SYSTEM_UID = os.getenv("SYSTEM_UID", "IamBatman")

        self.VIRUS_ANALYZER_API = os.getenv("ALLOWED_EXTENSIONS", None)
        allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "pdf")
        self.ALLOWED_EXTENSIONS = allowed_extensions.split(",")
        self.MAX_FILE_WEIGHT = os.getenv("MAX_FILE_WEIGHT", 16000)
        self.DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d")
        self.TIME_FORMAT = os.getenv("TIME_FORMAT", "%H:%M:%S")
        self.DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")

        self.KAFKA_HOST = os.getenv("KAFKA_HOST", "172.25.0.2")
        self.KAFKA_PORT = os.getenv("KAFKA_PORT", 9092)

        self.MONGO_HOST = os.getenv("MONGO_HOST", "127.0.0.1")
        self.MONGO_PORT = os.getenv("MONGO_PORT", 27017)
        self.MONGO_USER = os.getenv("MONGO_USER", "mongo")
        self.MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "mongo")
        self.MONGO_COLLECTION = os.getenv("MONGO_COLLECTION", "dev")

        self.KAFKA_PREFIX = "task:" + self.API_VERSION
