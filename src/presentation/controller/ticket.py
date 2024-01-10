from ...application.ticket import TicketApplication
from ...domain.model.ticket import Ticket, TicketIdentifier
from ...infrastructure.broker.BrokerMock import BrokerMock
from ...infrastructure.repositories.ticket_mongo import Ticket as TicketRepository
from ...utils.ResponseHandler import ID_NOT_VALID
from ..BrokerProtocol import BrokerProtocol
from ..ExceptionHandler import exception_handler
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
        _r = TicketRepository() if ref_repository is None else ref_repository
        _b = BrokerMock.setToDefault() if ref_broker is None else ref_broker
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

    @exception_handler
    def fetch(self) -> list:
        return self._uc.fetch()

    @exception_handler
    def getById(self, identifier):
        try:
            ticketId = TicketIdentifier(identifier)
        except ValueError:
            raise PresentationError(ID_NOT_VALID)

        self._uc.getById(ticketId)

    @exception_handler
    def delete(self, identifier):
        try:
            ticketId = TicketIdentifier(identifier)
        except ValueError:
            raise PresentationError(ID_NOT_VALID)

        self.delete(ticketId)

    @exception_handler
    def update(self, identifier, params: dict):
        try:
            ticketId = TicketIdentifier(identifier)
        except ValueError:
            raise PresentationError(ID_NOT_VALID)

        self.update(ticketId, params)

    @exception_handler
    def create(self, ticketId, description):
        obj = Ticket.newTicket(ticketId, description)
        return self._uc.create(obj)
