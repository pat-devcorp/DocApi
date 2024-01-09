from utils.ResponseHandler import REQUIRED_FIELD
from ..PresentationError import PresentationError
from ..BrokerProtocol import BrokerProtocol
from ..RepositoryProtocol import RepositoryProtocol

from ...application.ticket import TicketApplication
from ...domain.model.ticket import TicketDto, TicketIdentifier
from ...infrastructure.broker.kafka import Kafka
from ...infrastructure.repositories.ticket_mongo import Ticket as TicketRepository
from ..ExceptionHandler import exception_handler


class TicketController:
    def __init__(
        self,
        ref_write_uid,
        ref_repository: None | RepositoryProtocol = None,
        ref_broker: None | BrokerProtocol = None,
    ) -> None:
        _w = ref_write_uid
        _r = TicketRepository() if ref_repository is None else ref_repository
        _b = Kafka.setToDefault() if ref_broker is None else ref_broker
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
        objId = TicketIdentifier(identifier)
        self._uc.getById(objId)
    
    @exception_handler
    def delete(self, identifier):
        objId = TicketIdentifier(identifier)
        self.delete(objId)

    @exception_handler
    def update(self, params: dict):
        if ticketId := params.get('ticketId'):
            raise PresentationError(REQUIRED_FIELD, "ticket id must be provided")
        obj = TicketDto.fromDict(params)
        self.update(obj)

    @exception_handler
    def create(self, params: dict):
        if ticketId := params.get('ticketId'):
            raise PresentationError(REQUIRED_FIELD, "ticket id must be provided")
        if description := params.get('description'):
            raise PresentationError(REQUIRED_FIELD, "description must be")
        obj = TicketDto.newTicket(ticketId, description)
        return self._uc.create(obj)

    # def addKeyword(self, ticketId: IdentifierHandler, keyword_id: IdentifierHandler):
    #     return self._uc.addKeyword(ticketId.value, keyword_id.value)

    # def removeKeyword(self, ticketId: IdentifierHandler, keyword_id: IdentifierHandler):
    #     pass

    # def addMeeting(self, ticketId: IdentifierHandler, meeting_id: IdentifierHandler):
    #     pass

    # def removeMeeting(self, ticketId: IdentifierHandler, meeting_id: IdentifierHandler):
    #     pass

    # def addMilestone(self, ticketId: IdentifierHandler, milestone_id: IdentifierHandler):
    #     pass

    # def removeMilestone(
    #     self, ticketId: IdentifierHandler, milestone_id: IdentifierHandler
    # ):
    #     pass

    # def addAttachment(self, ticketId: IdentifierHandler, file_name: FileHanlder):
    #     pass

    # def removeAttachment(self, ticketId: IdentifierHandler, file_name: FileHanlder):
    #     pass

    # def addMember(self, ticketId: IdentifierHandler, member_id: IdentifierHandler):
    #     pass

    # def removeMember(self, ticketId: IdentifierHandler, member_id: IdentifierHandler):
    #     pass

    # def setAssignee(self, ticketId: IdentifierHandler, member_id: IdentifierHandler):
    #     pass
