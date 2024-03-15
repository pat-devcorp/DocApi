from ...application.ticket import TicketApplication
from ...domain.model.ticket import TicketDomain
from ...infrastructure.broker.MockBroker import MockBroker
from ...infrastructure.config import Config
from ...infrastructure.mongo.repositories.ticket_mongo import TicketMongo
from ...utils.timeout import timeout_function, TimeoutError
from ..BrokerProtocol import BrokerProtocol
from ..RepositoryProtocol import RepositoryProtocol


class TicketController:
    def __init__(
        self,
        ref_write_uid,
        ref_repository: None | RepositoryProtocol = None,
        ref_broker: None | BrokerProtocol = None,
    ) -> None:
        _w = ref_write_uid
        my_config = Config()
        _r = TicketMongo(my_config) if ref_repository is None else ref_repository
        _b = MockBroker.set_default(my_config) if ref_broker is None else ref_broker
        self._app = TicketApplication(_w, _r, _b)

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
        return timeout_function(self._app.fetch, args=(0), seconds=600)

    def get_by_id(self, obj_id):
        ticketId = TicketDomain.set_identifier(obj_id)

        return timeout_function(self._app.get_by_id, args=(ticketId), seconds=600)

    def delete(self, obj_id):
        ticketId = TicketDomain.set_identifier(obj_id)

        return timeout_function(self._app.delete, args=(ticketId), seconds=600)

    def update(self, obj_id, params: dict):
        ticketId = TicketDomain.set_identifier(obj_id)
        obj = TicketDomain.partial_ticket(ticketId, params)
        
        return timeout_function(self._app.update, args=(obj), seconds=600)

    def create(self, obj_id, description):
        ticketId = TicketDomain.set_identifier(obj_id)
        obj = TicketDomain.new_ticket(ticketId, description)

        return timeout_function(self._app.create, args=(obj), seconds=600)
