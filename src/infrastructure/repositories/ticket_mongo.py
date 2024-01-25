from ..InfrastructureError import InfrastructureError
from .mongo import Mongo, MongoServer


class TicketMongo:
    tablename = "ticket"
    pk = "ticketId"

    def __init__(
        self, ref_mongo: MongoServer | None = None
    ) -> None | InfrastructureError:
        self._m = (
            Mongo.set_default(self.tablename, self.pk)
            if ref_mongo is None
            else Mongo(ref_mongo)
        )

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
