from ..struct.audit import Audit as AuditStruct
from ..struct.ticket import Ticket as TicketDomain
from ..struct.ticket import TicketStruct
from ..struct.ticket import StateTicket, EventTicket
from .audit import Audit as AuditUseCase
from .repositoryProtocol import RepositoryProtocol


class Ticket:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self._fields = TicketStruct._fields
    

    def stateMachine(self, state: StateTicket, event: EventTicket):
        if state.CREATED:
            if event.CREATED:
                self.state = StateTicket.CREATED

    def setFields(self, fields: list):
        self._fields = [
            field for field in fields if field in TicketStruct._fields
        ]

    def getAll(self):
        return self.my_repository.get(TicketStruct.__name__, self._fields)
    
    def getByID(self, value):
        return self.my_repository.getByID(
            TicketStruct.__name__, "_id", value, self._fields
        )

    def create(self, ref_dto: dict):
        my_dto = {k: v for k, v in ref_dto.items() if k in TicketStruct._fields}
        my_audit = AuditUseCase(self.my_repository)
        ref_audit = my_audit.create(my_dto)
        print(ref_audit)
        ref_dto.update({"audit": ref_audit._id})

        my_ticket_struct = TicketDomain.fromDict(ref_dto)
        my_ticket_struct.create()

        self.my_repository.create(self.__name__, my_ticket_struct.asDict())

        return my_ticket_struct.asDict()

    def update(self, ref_dto: dict):
        my_dto = {k: v for k, v in ref_dto.items() if k in TicketStruct._fields}
        my_audit = AuditUseCase(self.my_repository)
        my_audit.update(my_dto)

        data = self.getByID(ref_dto._id)
        my_ticket_struct = TicketDomain.fromDict(data)
        my_ticket_struct.update()

        self.my_repository.update(
            TicketStruct.__name__, "_id", str(ref_dto._id), my_ticket_struct.asDict()
        )

        return my_ticket_struct.asDict()
