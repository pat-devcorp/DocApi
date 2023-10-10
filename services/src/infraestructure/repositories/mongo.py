from typing import Dict, List

from pymongo import MongoClient

from ..config import Config
from .RepositoryError import RepositoryError


class Mongo:
    connection = None
    client = None

    def __init__(
        self,
        server_address: str,
        port: int,
        user: str,
        password: str,
        database: str = None,
    ):
        self.server_address = server_address
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    @property
    def chain_connection(self):
        return (
            f"mongodb://{self.user}:{self.password}@"
            f"{self.server_address}:{self.port}"
        )

    @classmethod
    def setToDefault(cls):
        my_config = Config()
        return cls(
            my_config.MONGO_HOST,
            my_config.MONGO_PORT,
            my_config.MONGO_USER,
            my_config.MONGO_PASSWORD,
            my_config.MONGO_DATABASE,
        )

    def startConnection(self):
        try:
            self.connection = MongoClient(self.chain_connection)
            self.client = self.connection[self.database]
        except Exception as err:
            raise RepositoryError(
                f"{self.chain_connection}\n{str(err)}",
            )

    def getCollection(self, tablename: str):
        self.startConnection()
        if self.client is None:
            raise RepositoryError("Connection not established")
        return self.client[tablename]

    def get(self, tablename: str, attrs: List[str]) -> List[Dict]:
        collection = self.getCollection(tablename)
        try:
            return list(collection.find({}, {attr: 1 for attr in attrs}))
        except Exception as err:
            raise RepositoryError(str(err))

    def getByID(self, tablename: str, pk: str, id_val: str, attrs: List[str]) -> Dict:
        collection = self.getCollection(tablename)
        try:
            return collection.find_one({pk: id_val}, {attr: 1 for attr in attrs})
        except Exception as err:
            raise RepositoryError(str(err))

    def update(self, tablename: str, pk: str, id_val: str, kwargs: dict):
        collection = self.getCollection(tablename)
        if not self.getByID(tablename, pk, id_val, []):
            raise RepositoryError(
                f"No record found for ID {id_val} not found in table {tablename}"
            )
        collection.update_one({pk: id_val}, {"$set": kwargs})

    def create(self, tablename: str, kwargs: dict):
        collection = self.getCollection(tablename)
        collection.insert_one(kwargs)
