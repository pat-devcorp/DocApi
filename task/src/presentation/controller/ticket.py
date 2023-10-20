from ...application.ticket import Ticket as TicketUseCase
from ...application.ticket import TicketEvent
from ...infraestructure.broker.kafka import Kafka
from ...infraestructure.repositories.mongo import Mongo


class Ticket:
    def __init__(self, ref_repository=None, ref_producer=None):
        self._repository = (
            Mongo.setToDefault() if ref_repository is None else ref_repository
        )
        self._producer = (
            Kafka.setToDefault() if ref_producer is None else ref_producer
        )
        self._use_case = TicketUseCase(self._repository, self._producer)

    @staticmethod
    def getTemplate() -> str:
        return """
            **YO:** Patrick Alonso Fuentes Carpio

            **COMO:** Usuario del módulo de Administración

            **QUIERO:** Generar una nueva tarea en el dashboard para desarrollo que me indique la conformidad del requerimiento.

            **PORQUE:** Mejorar la trazabilidad y proporcionar estadísticas reales.

            **HITO:** Recibir un correo que confirme la culminación de la tarea.

            **ANOTACIONES:** Las áreas afectadas serán sistemas y desarrollo en el módulo dashboard.
            """

    def fetch(self) -> list:
        datos = self._use_case.fetch()
        return datos

    def getByID(self, ref_ticket) -> dict:
        data = self._use_case.getByID(ref_ticket)
        return data

    def create(self, ref_ticket):
        my_ticket = self._use_case.stateMachine(TicketEvent.CREATED, ref_ticket)
        return my_ticket

    def update(self, ref_ticket):
        my_ticket = self._use_case.stateMachine(TicketEvent.UPDATED, ref_ticket)
        return my_ticket

    def delete(self, ref_ticket):
        my_ticket = self._use_case.stateMachine(TicketEvent.DELETED, ref_ticket)
        return my_ticket
