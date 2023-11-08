from ...application.ticket import Ticket as TicketUseCase
from ...infraestructure.broker.kafka import Kafka
from ...infraestructure.repositories.mongo import Mongo
from ...utils.FileHandler import FileHanlder
from ...utils.IdentityHandler import IdentityHandler
from ..interface.ticket import TicketDTO


class Ticket:
    def __init__(self, ref_write_uid, ref_repository=None, ref_producer=None):
        self._w = ref_write_uid
        self._r = Mongo.setToDefault() if ref_repository is None else ref_repository
        self._p = Kafka.setToDefault() if ref_producer is None else ref_producer
        self._uc = TicketUseCase(self._w, self._r, self._p)

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
        datos = self._uc.fetch()
        return datos

    def create(self, ref_object: TicketDTO):
        return self._uc.create(ref_object)

    def update(self, ref_object: TicketDTO):
        return self._uc.update(ref_object)

    def getByID(self, ticket_id: IdentityHandler) -> dict:
        data = self._uc.getByID(ticket_id)
        return data

    def delete(self, ticket_id: IdentityHandler):
        return self._uc.delete(ticket_id)

    def addKeyword(self, ticket_id: IdentityHandler, keyword_id: IdentityHandler):
        return self._uc.addKeyword(ticket_id, keyword_id)

    def removeKeyword(self, ticket_id: IdentityHandler, keyword_id: IdentityHandler):
        pass

    def addMeeting(self, ticket_id: IdentityHandler, meeting_id: IdentityHandler):
        pass

    def removeMeeting(self, ticket_id: IdentityHandler, meeting_id: IdentityHandler):
        pass

    def addMilestone(self, ticket_id: IdentityHandler, milestone_id: IdentityHandler):
        pass

    def removeMilestone(
        self, ticket_id: IdentityHandler, milestone_id: IdentityHandler
    ):
        pass

    def addAttachment(self, ticket_id: IdentityHandler, file_name: FileHanlder):
        pass

    def removeAttachment(self, ticket_id: IdentityHandler, file_name: FileHanlder):
        pass

    def addMember(self, ticket_id: IdentityHandler, member_id: IdentityHandler):
        pass

    def removeMember(self, ticket_id: IdentityHandler, member_id: IdentityHandler):
        pass

    def setAssignee(self, ticket_id: IdentityHandler, member_id: IdentityHandler):
        pass
