from ...application.ticket import Ticket as TicketUseCase
from ...application.ticket import TicketEvent
from ...infraestructure.kafka import Kafka
from ...infraestructure.repositories.mongo import Mongo
from ..interface.ticket import TicketDTO


class Ticket:
    def __init__(self, ref_repository=None, ref_producer=None):
        self._repository = (
            Mongo.setToDefault() if ref_repository is None else ref_repository
        )
        self._producer = (
            Kafka.setToDefault() if ref_producer is None else ref_producer
        )
        self._use_case = TicketUseCase(self._repository, self._producer)

    def get(self) -> list:
        datos = self._use_case.get()
        return datos

    def getByID(self, ref_ticket: TicketDTO) -> dict:
        data = self._use_case.getByID(ref_ticket)
        return data

    def create(self, ref_ticket: TicketDTO):
        my_ticket = self._use_case.stateMachine(TicketEvent.CREATED, ref_ticket)
        return my_ticket

    def update(self, ref_ticket: TicketDTO):
        my_ticket = self._use_case.stateMachine(TicketEvent.UPDATED, ref_ticket)
        return my_ticket

    def delete(self, ref_ticket: TicketDTO):
        my_ticket = self._use_case.stateMachine(TicketEvent.DELETED, ref_ticket)
        return my_ticket
