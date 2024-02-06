import os

from .singleton import singleton


@singleton
class Config:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_PATH = os.path.abspath(os.path.join(current_directory, ".."))
        self.ROUTE_PATH = os.path.join("src", "rest", "route")
        self.LOG_PATH = os.path.join("src", "log", "api", "api.log")
        self.LOG_CONFIG = os.path.join(
            self.PROJECT_PATH, "infrastructure", "logger", "logging_config.json"
        )
        self.SECRET_KEY = os.getenv("SECRET_KEY", "BatmanIsBruceWayne")
        self.API_VERSION = os.getenv("API_VERSION", "1.0.0.0")
        self.NAME = "task_" + self.API_VERSION
        self.IS_IN_PRODUCTION = os.getenv("IS_IN_PRODUCTION", 0)
        self.SYSTEM_UID = os.getenv("SYSTEM_UID", "IamBatman")

        self.VIRUS_ANALYZER_API = os.getenv("ALLOWED_EXTENSIONS", None)
        allowed_extensions = os.getenv("ALLOWED_EXTENSIONS", "pdf")
        self.ALLOWED_EXTENSIONS = allowed_extensions.split(",")
        self.MAX_FILE_WEIGHT = os.getenv("MAX_FILE_WEIGHT", 16000)
        self.DATE_FORMAT = os.getenv("DATE_FORMAT", "%Y-%m-%d")
        self.TIME_FORMAT = os.getenv("TIME_FORMAT", "%H:%M:%S")
        self.DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", "%Y-%m-%d %H:%M:%S")

        self.BROKER = os.getenv("BROKER", False)
        self.BROKER_LOST_MESSAGE_PATH = os.getenv(
            "BROKER_LOST_MESSAGE_PATH", os.path.join("src", "log", "broker", "lost")
        )
        if self.BROKER == "RABBITMQ":
            self.RABBITMQ_HOST = os.environ["RABBITMQ_HOST"]
            self.RABBITMQ_PORT = os.environ["RABBITMQ_PORT"]
            self.RABBITMQ_USER = os.environ["RABBITMQ_USER"]
            self.RABBITMQ_PASS = os.environ["RABBITMQ_PASS"]
        if self.BROKER == "KAFKA":
            self.KAFKA_HOST = os.environ["KAFKA_HOST"]
            self.KAFKA_PORT = os.environ["KAFKA_PORT"]

        self.DB = os.getenv("DB", False)
        if self.DB == "MONGO":
            self.MONGO_HOST = os.environ["MONGO_HOST"]
            self.MONGO_PORT = os.environ["MONGO_PORT"]
            self.MONGO_USER = os.environ["MONGO_USER"]
            self.MONGO_PASS = os.environ["MONGO_PASS"]
            self.MONGO_DB = os.environ["MONGO_DB"]
