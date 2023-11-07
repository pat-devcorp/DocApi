from typing import Dict, List

from pymongo import MongoClient

from ..config import Config
from ..InfraestructureError import InfraestructureError


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
            f"{self.server_address}:{self.port}/?authMechanism=DEFAULT"
        )

    @classmethod
    def setToDefault(cls):
        my_config = Config()
        return cls(
            my_config.MONGO_HOST,
            my_config.MONGO_PORT,
            my_config.MONGO_USER,
            my_config.MONGO_PASSWORD,
            my_config.MONGO_COLLECTION,
        )

    def startConnection(self):
        try:
            self.connection = MongoClient(self.chain_connection)
            self.client = self.connection[self.database]
        except Exception as err:
            raise InfraestructureError(
                f"{self.chain_connection}\n{str(err)}",
            )

    def getCollection(self, tablename: str):
        self.startConnection()
        if self.client is None:
            raise InfraestructureError("Connection not established")
        return self.client[tablename]

    def fetch(self, tablename: str, pk_name: str, attrs: List[str]) -> List[Dict]:
        collection = self.getCollection(tablename)
        try:
            datos = list(collection.find({}, {attr: 1 for attr in attrs}))
            for item in datos:
                item[pk_name] = item.pop("_id")
            return datos
        except Exception as err:
            raise InfraestructureError(str(err))

    def getByID(
        self, tablename: str, pk_name: str, id_val: str, attrs: List[str]
    ) -> Dict:
        collection = self.getCollection(tablename)
        try:
            data = collection.find_one({"_id": id_val}, {attr: 1 for attr in attrs})
            data[pk_name] = data.pop("_id")
            return data
        except Exception as err:
            raise InfraestructureError(str(err))

    def update(self, tablename: str, pk_name: str, id_val: str, kwargs: dict):
        collection = self.getCollection(tablename)
        if not self.getByID(tablename, pk_name, id_val, []):
            raise InfraestructureError(
                f"No record found for ID {id_val} not found in table {tablename}"
            )
        collection.update_one({"_id": id_val}, {"$set": kwargs})

    def create(self, tablename: str, pk_name: str, kwargs: dict):
        data = kwargs
        data["_id"] = data.pop(pk_name)
        collection = self.getCollection(tablename)
        collection.insert_one(data)

    def delete(self, tablename: str, pk_name: str, id_val: str) -> bool:
        collection = self.getCollection(tablename)
        if not self.getByID(tablename, pk_name, id_val, []):
            raise InfraestructureError(
                f"No record found for ID {id_val} not found in table {tablename}"
            )
        collection.delete_one({pk_name: id_val})
