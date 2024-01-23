from typing import Dict, List

from pydantic import BaseModel
from pymongo import MongoClient

from ...utils.ResponseHandler import DB_CREATE_FAIL, DB_DELETE_FAIL, DB_UPDATE_FAIL
from ..config import Config
from ..InfrastructureError import InfrastructureError


class MongoServer(BaseModel):
    hostname: str
    port: int
    username: str
    password: str
    collection: str
    tablename: str
    pk: str


class Mongo:
    def __init__(self, ref_mongo_server: MongoServer):
        self.server = ref_mongo_server
        self.pk = ref_mongo_server.pk
        self.client = None
        self.collection = None

    @property
    def getDSN(self):
        return f"mongodb://{self.server.username}:{self.server.password}@{self.server.hostname}:{self.server.port}"

    def _connect(self):
        if self.client is None:
            self.client = MongoClient(self.getDSN)
            self.collection = self.client[self.server.collection][
                self.server.tablename
            ]  # Access collection directly

    @property
    def cursor(self):
        self._connect()
        return self.collection  # Use collection as cursor

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            self.client.close()
            self.client = None

    @classmethod
    def setDefault(cls, tablename, pk):
        my_config = Config()
        con = MongoServer(
            hostname=my_config.MONGO_HOST,
            port=my_config.MONGO_PORT,
            username=my_config.MONGO_USER,
            password=my_config.MONGO_PASS,
            collection=my_config.MONGO_DB,
            tablename=tablename,
            pk=pk,
        )
        return cls(con)

    def fetch(self, attrs: List[str]) -> List[Dict] | InfrastructureError:
        data = list(self.cursor.find({}, {attr: 1 for attr in attrs}))
        for item in data:
            item[self.pk] = item.pop("_id")
        return data

    def getById(
        self, identifier: str, attrs: List[str]
    ) -> Dict | None | InfrastructureError:
        item = self.cursor.find_one({"_id": identifier}, {attr: 1 for attr in attrs})
        if item:
            item[self.pk] = item.pop("_id")
        return item

    def delete(self, identifier: str):
        try:
            self.cursor.delete_one({"_id": identifier})
        except Exception as err:
            raise InfrastructureError(DB_DELETE_FAIL, str(err))

    def update(self, identifier: str, kwargs: dict):
        try:
            self.cursor.update_one({"_id": identifier}, {"$set": kwargs})
        except Exception as err:
            raise InfrastructureError(DB_UPDATE_FAIL, str(err))

    def create(self, kwargs: dict):
        try:
            kwargs["_id"] = kwargs.pop(self.pk)
            self.cursor.insert_one(kwargs)
        except Exception as err:
            raise InfrastructureError(DB_CREATE_FAIL, str(err))


# Test
def mongoTestingInterface():
    mongo_repository = Mongo.setDefault("test", "identifier")
    print(f"CONNECTION: {mongo_repository.getDSN}")

    current_id = "87378a1e-894c-11ee-b9d1-0242ac120002"
    dto = {
        "writeUId": "8888",
        "identifier": current_id,
        "description": "This is description",
    }
    mongo_repository.create(dto)

    data = mongo_repository.fetch(dto.keys())
    assert data

    text = "It was modified"
    mongo_repository.update(current_id, {"description": text})

    item = mongo_repository.getById(current_id, ["description"])
    assert item["description"] == text

    mongo_repository.delete(current_id)
    assert mongo_repository.getById(current_id, ["description"]) is None
