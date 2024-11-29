import os


class Environment:
    ApiVersion: str
    DockerName: str
    DockerTag: str
    SecretKey: str
    ApiHost: str
    ApiPort: int
    RpcPort: int
    AllowedExtensions: list
    MaxFileWeight: int
    ContextTimeOut: int
    MongoHost: str
    MongoPort: int
    MongoUser: str
    MongoPassword: str
    MongoDatabase: str
    RabbitmqHost: str
    RabbitmqPort: int
    RabbitmqUser: str
    RabbitmqPassword: str

    def __init__(self):
        self.ApiVersion = os.environ["API_BASE_VERSION"]
        self.DockerName = os.environ["DOCKER_NAME"]
        self.DockerTag = os.environ["DOCKER_TAG"]
        self.SecretKey = os.environ["APP_SECRET"]
        self.ApiHost = os.environ["API_HOST"]
        self.ApiPort = os.environ["API_PORT"]
        self.RpcPort = os.environ["RPC_PORT"]
        self.MaxFileWeight = os.environ["MAX_FILE_WEIGHT"]
        self.ContextTimeOut = os.environ["TIME_OUT"]

        self.IsInProduction = os.getenv("IS_IN_PRODUCTION", 0)
        str_extensions = os.environ["ALLOWED_EXTENSIONS"]
        self.AllowedExtensions = str_extensions.split(",")

        self.MongoHost = os.getenv("MONGO_HOST")
        self.MongoPort = os.getenv("MONGO_PORT")
        self.MongoUser = os.getenv("MONGO_USER")
        self.MongoPassword = os.getenv("MONGO_PASS")
        self.MongoDatabase = os.getenv("MONGO_DB")
        self.RabbitmqHost = os.getenv("RABBITMQ_HOST")
        self.RabbitmqPort = os.getenv("RABBITMQ_PORT")
        self.RabbitmqUser = os.getenv("RABBITMQ_USER")
        self.RabbitmqPassword = os.getenv("RABBITMQ_PASS")

    def get_paths(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.PROJECT_PATH = os.path.abspath(os.path.join(current_directory, "..", ".."))
        self.ROUTE_PATH = os.path.join(self.PROJECT_PATH, "rest", "route")
        self.LOG_PATH = os.path.join(self.PROJECT_PATH, "log", "api", "task.log")
        self.BROKER_PATH = os.path.join(self.PROJECT_PATH, "log", "broker")
        self.IMAGE_PATH = os.path.join(self.PROJECT_PATH, "media", "img")
        self.LOG_CONFIG = os.path.join(
            self.PROJECT_PATH, "infrastructure", "logger", "config.json"
        )
