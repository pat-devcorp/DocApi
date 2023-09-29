from ..struct.audit import Audit as AuditStruct
from ..struct.ticket import Ticket as TicketStruct
from ..struct.ticket import StateTicket, EventTicket
from .audit import Audit as AuditUseCase
from .repositoryProtocol import RepositoryProtocol


class Ticket:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self.__fields__ = TicketStruct.__fields__
    

    def stateMachine(self, state: StateTicket, event: EventTicket):
        if state.CREATED:
            if event.CREATED:
                self.state = StateTicket.CREATED

    def setFields(self, fields: list):
        self.__fields__ = [
            field for field in fields if field in TicketStruct.__fields__
        ]

    def getAll(self):
        return self.my_repository.get(TicketStruct.__tablename__, self.__fields__)
    
    def getByID(self, value):
        return self.my_repository.getByID(
            TicketStruct.__tablename__, "_id", value, self.__fields__
        )

    def create(self, ref_dto: dict):
        my_dto = {k: v for k, v in ref_dto.items() if k in AuditStruct.__fields__}
        my_audit = AuditUseCase(self.my_repository)
        ref_audit = my_audit.create(my_dto)
        print(ref_audit)
        ref_dto.update({"audit": ref_audit._id})

        my_ticket_struct = TicketStruct.fromDict(ref_dto)
        my_ticket_struct.create()

        self.my_repository.create(self.__tablename__, my_ticket_struct.asDict())

        return my_ticket_struct.asDict()

    def update(self, ref_dto: dict):
        my_dto = {k: v for k, v in ref_dto.items() if k in AuditStruct.__fields__}
        my_audit = AuditUseCase(self.my_repository)
        my_audit.update(my_dto)

        data = self.getByID(ref_dto._id)
        my_ticket_struct = TicketStruct.fromDict(data)
        my_ticket_struct.update()

        self.my_repository.update(
            TicketStruct.__tablename__, "_id", str(ref_dto._id), my_ticket_struct.asDict()
        )

        return my_ticket_struct.asDict()
