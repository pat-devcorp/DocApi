from ...InfrastructureError import InfrastructureError
from ..mongo import Mongo, MongoConfig


class TicketMongo:
    tablename = "ticket"
    pk = "ticketId"

    def __init__(self, my_config: MongoConfig) -> None | InfrastructureError:
        self._m = Mongo.set_default(my_config, self.tablename, self.pk)

    def entity_exists(self, identifier) -> bool:
        if self._m.get_by_id(identifier, [self._pk]) is None:
            return False
        return True

    def fetch(self, fields: list, matching) -> list:
        return self._m.fetch(fields, matching)

    def get_by_id(self, identifier, fields: list) -> dict:
        return self._m.get_by_id(identifier, fields)

    def delete(self, identifier) -> None | InfrastructureError:
        self._m.delete(identifier)
        return None

    def update(self, identifier, data) -> None | InfrastructureError:
        self._m.update(identifier, data)
        return None

    def create(self, data) -> None | InfrastructureError:
        self._m.create(data)
        return None
