from ...domain.model.ticket import Ticket
from ..InfrastructureError import InfrastructureError
from .mongo import Mongo, MongoServer


class TicketMongo:
    tablename = "ticket"
    pk = "ticketId"

    def __init__(
        self, ref_mongo: MongoServer | None = None
    ) -> None | InfrastructureError:
        self._m = (
            Mongo.setDefault(self.tablename, self.pk)
            if ref_mongo is None
            else Mongo(ref_mongo)
        )
        self._f = Ticket.getFields()

    def entityExists(self, identifier) -> None | InfrastructureError:
        if self._m.getById(identifier, [self._pk]) is None:
            return False
        return True

    def fetch(self, fields=None) -> list:
        return self._m.fetch(fields or self._f)

    def getById(self, identifier, fields=None) -> list:
        return self._m.getById(identifier, fields or self._f)

    def delete(self, identifier) -> None | InfrastructureError:
        self._m.delete(identifier)
        return True

    def update(self, identifier, data) -> None | InfrastructureError:
        self._m.update(identifier, data)
        return True

    def create(self, data) -> None | InfrastructureError:
        self._m.create(data)
        return True
