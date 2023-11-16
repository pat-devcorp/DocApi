from collections import namedtuple
from typing import Dict, List

from pymongo import MongoClient

from ..config import Config
from ..InfraestructureError import InfraestructureError

MongoDTO = namedtuple(
    "MongoDTO", ["server_address", "port", "user", "password", "database"]
)


class Mongo:
    connection = None
    client = None

    def __init__(self, mongo_dto: MongoDTO):
        self.server_address = mongo_dto.server_address
        self.port = mongo_dto.port
        self.user = mongo_dto.user
        self.password = mongo_dto.password
        self.database = mongo_dto.database

    @property
    def chain_connection(self):
        return (
            f"mongodb://{self.user}:{self.password}@"
            f"{self.server_address}:{self.port}/?authMechanism=DEFAULT"
        )

    @classmethod
    def setToDefault(cls):
        my_config = Config()
        con = MongoDTO(
            my_config.MONGO_HOST,
            my_config.MONGO_PORT,
            my_config.MONGO_USER,
            my_config.MONGO_PASSWORD,
            my_config.MONGO_COLLECTION,
        )
        return cls(con)

    def startConnection(self) -> bool | InfraestructureError:
        try:
            self.connection = MongoClient(self.chain_connection)
            self.client = self.connection[self.database]
            return True
        except Exception as err:
            raise InfraestructureError(
                f"{self.chain_connection}\n{str(err)}",
            )

    def getCollection(self, tablename: str):
        self.startConnection()
        if self.client is None:
            raise InfraestructureError("Connection not established")
        return self.client[tablename]

    def fetch(
        self, tablename: str, pk_name: str, attrs: List[str]
    ) -> List[Dict] | InfraestructureError:
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
    ) -> Dict | InfraestructureError:
        collection = self.getCollection(tablename)
        try:
            data = collection.find_one({"_id": id_val}, {attr: 1 for attr in attrs})
            data[pk_name] = data.pop("_id")
            return data
        except Exception as err:
            raise InfraestructureError(str(err))

    def update(self, tablename: str, pk_name: str, id_val: str, kwargs: dict):
        collection = self.getCollection(tablename)
        data = kwargs
        data["_id"] = data.pop(pk_name)
        collection.update_one({"_id": id_val}, {"$set": kwargs})

    def create(self, tablename: str, pk_name: str, kwargs: dict):
        data = kwargs
        data["_id"] = data.pop(pk_name)
        collection = self.getCollection(tablename)
        collection.insert_one(data)

    def delete(self, tablename: str, pk_name: str, id_val: str):
        collection = self.getCollection(tablename)
        collection.delete_one({pk_name: id_val})
