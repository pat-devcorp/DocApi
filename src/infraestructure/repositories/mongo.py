from collections import namedtuple
from typing import Dict, List

from pymongo import MongoClient

from ...utils.ErrorHandler import (
    DB_COLLECTION_NOT_FOUND,
    DB_CONNECTION_ERROR,
    DB_CREATE_FAIL,
    DB_DELETE_FAIL,
    DB_GET_FAIL,
    DB_UPDATE_FAIL,
    ID_NOT_FOUND,
)
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
                DB_CONNECTION_ERROR,
                f"{self.chain_connection}\n{str(err)}",
            )

    def getCollection(self, tablename: str):
        self.startConnection()
        if self.client is None:
            raise InfraestructureError(
                DB_COLLECTION_NOT_FOUND, "Connection not established"
            )
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
            raise InfraestructureError(DB_GET_FAIL, str(err))

    def getByID(
        self, tablename: str, pk_name: str, id_val: str, attrs: List[str]
    ) -> Dict | InfraestructureError:
        collection = self.getCollection(tablename)
        try:
            data = collection.find_one({"_id": id_val}, {attr: 1 for attr in attrs})
            data[pk_name] = data.pop("_id")
            return data
        except Exception as err:
            raise InfraestructureError(ID_NOT_FOUND, str(err))

    def update(self, tablename: str, pk_name: str, id_val: str, kwargs: dict):
        collection = self.getCollection(tablename)
        try:
            collection.update_one({"_id": id_val}, {"$set": kwargs})
        except Exception as err:
            raise InfraestructureError(DB_UPDATE_FAIL, str(err))

    def create(self, tablename: str, pk_name: str, kwargs: dict):
        data = kwargs
        data["_id"] = data.pop(pk_name)
        collection = self.getCollection(tablename)
        try:
            collection.insert_one(data)
        except Exception as err:
            raise InfraestructureError(DB_CREATE_FAIL, str(err))

    def delete(self, tablename: str, pk_name: str, id_val: str):
        collection = self.getCollection(tablename)
        try:
            collection.delete_one({pk_name: id_val})
        except Exception as err:
            raise InfraestructureError(DB_DELETE_FAIL, str(err))
