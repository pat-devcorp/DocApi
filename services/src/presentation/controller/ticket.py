from ...application.ticket import Ticket as TicketUseCase
from ...application.ticket import TicketEvent
from ...infraestructure.producer import Producer
from ...infraestructure.repositories.mongo import Mongo
from ..interface.ticket import TicketDTO


class Ticket:
    _repository = None

    def __init__(self, ref_repository=None, ref_producer=None):
        self._repository = (
            Mongo.setToDefault() if ref_repository is None else ref_repository
        )
        self._producer = (
            Producer.setToDefault() if ref_producer is None else ref_producer
        )
        self._use_case = TicketUseCase(self._repository, self._producer)

    def getAll(self) -> list:
        datos = self._use_case.getAll()
        return datos

    def getByID(self, ticket_id) -> dict:
        data = self._use_case.getByID(ticket_id)
        return data

    def create(self, write_uid, ref_ticket: TicketDTO):
        my_ticket = self._use_case.stateMachine(
            write_uid, TicketEvent.CREATED, ref_ticket
        )
        return my_ticket

    def update(self, write_uid, ref_ticket: TicketDTO):
        my_ticket = self._use_case.stateMachine(
            write_uid, TicketEvent.UPDATED, ref_ticket
        )
        return my_ticket

    def delete(self, write_uid, ticket_id):
        my_ticket = self._use_case.stateMachine(
            write_uid, TicketEvent.DELETED, {"ticket_id": ticket_id}
        )
        return my_ticket
