from ...infraestructure.broker.kafka import Kafka
from ...infraestructure.repositories.mongo import Mongo
from ...application.ticket import Ticket as TicketUseCase
from ...application.ticket import TicketEvent
from ...utils.IdentityHandler import IdentityHandler
from ..interface.ticket import TicketDTO
from ..interface.keyword import KeywordDTO
from ..interface.meeting import MeetingDTO
from ..interface.member import MemberDTO
from ..interface.milestone import MilestoneDTO


class Ticket:
    def __init__(self, write_uid, ref_repository=None, ref_producer=None):
        self._write_uid = write_uid
        self._r = (
            Mongo.setToDefault() if ref_repository is None else ref_repository
        )
        self._p = (
            Kafka.setToDefault() if ref_producer is None else ref_producer
        )
        self._uc = TicketUseCase(self._r, self._p)


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
        datos = self._uc.fetch()
        return datos

    def create(self, ref_ticket: TicketDTO):
        my_ticket = self._uc.stateMachine(TicketEvent.CREATED, ref_ticket)
        return my_ticket

    def update(self, ref_ticket: TicketDTO):
        my_ticket = self._uc.stateMachine(TicketEvent.UPDATED, ref_ticket)
        return my_ticket
    
    def getByID(self, ticket_id: IdentityHandler) -> dict:
        data = self._uc.getByID(ticket_id)
        return data

    def delete(self, ticket_id: IdentityHandler):
        my_ticket = self._uc.stateMachine(TicketEvent.DELETED, ticket_id)
        return my_ticket
    
    def addKeyword(self, ticket_id: IdentityHandler, keyword: KeywordDTO):
        pass

    def removeKeyword(self, ticket_id: IdentityHandler, keyword_id: IdentityHandler):
        pass

    def addMeeting(self, ticket_id: IdentityHandler, meeting: MeetingDTO):
        pass

    def addMilestone(self, ticket_id: IdentityHandler, milestone: MilestoneDTO):
        pass

    def removeMilestone(self, ticket_id: IdentityHandler, milestone_id: IdentityHandler):
        pass

    def removeMeeting(self, ticket_id: IdentityHandler, meeting_id: IdentityHandler):
        pass

    def addAttachment(self, ticket_id: IdentityHandler, attachment_id: IdentityHandler):
        pass

    def removeAttachment(self, ticket_id: IdentityHandler, attachment_id: IdentityHandler):
        pass
    
    def addMember(self, ticket_id: IdentityHandler, member: MemberDTO):
        pass
    
    def removeMember(self, ticket_id: IdentityHandler, member_id: IdentityHandler):
        pass

    def setAssignee(self, ticket_id: IdentityHandler, member_id: IdentityHandler):
        pass