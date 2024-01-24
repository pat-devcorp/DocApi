from ...application.ticket import TicketApplication
from ...domain.model.ticket import TicketInterface
from ...infrastructure.broker.MockBroker import MockBroker
from ...infrastructure.repositories.ticket_mongo import TicketMongo
from ...utils.ResponseHandler import DEFAULT
from ..BrokerProtocol import BrokerProtocol
from ..PresentationError import PresentationError
from ..RepositoryProtocol import RepositoryProtocol


class TicketController:
    def __init__(
        self,
        ref_writeUId,
        ref_repository: None | RepositoryProtocol = None,
        ref_broker: None | BrokerProtocol = None,
    ) -> None:
        _w = ref_writeUId
        _r = TicketMongo() if ref_repository is None else ref_repository
        _b = MockBroker.setDefault() if ref_broker is None else ref_broker
        self._uc = TicketApplication(_w, _r, _b)

    @staticmethod
    def getTemplate() -> str:
        return """
            **I:** Patrick Alonso Fuentes Carpio

            **AS:** A developer, I need a task module.

            **I WANT TO:** Create a new task, associate users with different roles to the task, add meetings, link related words to the task for searching, conduct surveys, and maintain a list of milestones related to the task.

            **BECAUSE**: I want to enhance traceability and provide accurate statistics.

            **MILESTONES:**
            - Create, edit, and delete tasks.
            - Add team members.
            - Send notifications to team members based on task-related events.
            - Create surveys.
            - Schedule meetings.
            - Associate keywords with the task for searching.
            - Generate a task document.

            **NOTES:** The module should be developed following clean architecture principles.
            """

    def fetch(self) -> list:
        return self._uc.fetch()

    def getById(self, obj_id):
        ticketId = TicketInterface.setIdentifier(obj_id)
        self._uc.getById(ticketId)

    def delete(self, obj_id):
        ticketId = TicketInterface.setIdentifier(obj_id)
        self.delete(ticketId)

    def update(self, obj_id, params: dict):
        if params.get("ticketId") is not None:
            PresentationError(
                DEFAULT,
                "Id is not need in the params because you send as obj_id to the function",
            )
        print(f"ID: {type(obj_id), {obj_id}}")
        ticketId = TicketInterface.setIdentifier(obj_id)

        self.update(ticketId, params)

    def create(self, obj_id, description):
        ticketId = TicketInterface.setIdentifier(obj_id)
        obj = TicketInterface.newTicket(ticketId, description)

        return self._uc.create(obj)
