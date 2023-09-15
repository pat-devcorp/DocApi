from typing import Dict, List

from pymongo import MongoClient

from .repositoryError import repositoryError


class Mongo:
    def __init__(
        self,
        server_address: str,
        port: int,
        user: str,
        password: str,
        database: str,
    ):
        self.server_address = server_address
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.client = None

    @property
    def chain_connection(self):
        return (
            f"mongodb://{self.user}:{self.password}@"
            f"{self.server_address}:{self.port}"
        )

    def start_connection(self):
        try:
            self.connection = MongoClient(self.chain_connection)
            self.client = self.connection[self.database]
        except Exception as err:
            raise repositoryError(
                "MONGO: Invalid credentials",
                f"{self.chain_connection}\n{str(err)}",
            )

    def get_collection(self, tablename: str):
        self.start_connection()
        if self.client is None:
            raise repositoryError("MONGO: No Connection", "Connection not established")
        return self.client[tablename]

    def get(self, tablename: str, attrs: List[str]) -> List[Dict]:
        collection = self.get_collection(tablename)
        try:
            return list(collection.find({}, {attr: 1 for attr in attrs}))
        except Exception as err:
            raise repositoryError("MONGO: Bind", str(err))

    def get_by_id(self, tablename: str, pk: str, id_val: str, attrs: List[str]) -> Dict:
        collection = self.get_collection(tablename)
        try:
            return collection.find_one({pk: id_val}, {attr: 1 for attr in attrs})
        except Exception as err:
            raise repositoryError("MONGO: Bind", str(err))

    def update(self, tablename: str, pk: str, id_val: str, kwargs: dict):
        collection = self.get_collection(tablename)
        if not self.get_by_id(tablename, pk, id_val, []):
            raise repositoryError(
                "MONGO: No record found ", f"Id {id_val} not found in table {tablename}"
            )
        collection.update_one({pk: id_val}, {"$set": kwargs})

    def create(self, tablename: str, kwargs: dict):
        collection = self.get_collection(tablename)
        collection.insert_one(kwargs)
