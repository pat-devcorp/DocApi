from ...application.ticket import Ticket as TicketUseCase
from ...application.ticket import TicketEvent
from ...infraestructure.config import Config
from ...infraestructure.repositories.mongo import Mongo as MongoRepository
from ..interface.ticket import Ticket as TicketInterface
from ..interface.ticket import TicketStruct
from .ControllerError import ControllerError


class Ticket:
    my_repository = None

    def __init__(self, ref_repository=None):
        self.my_repository = (
            self.setToDefaultServer() if ref_repository is None else ref_repository
        )

    def setToDefaultServer(self):
        my_config = Config()
        self.my_repository = MongoRepository(
            my_config.MONGO_HOST,
            my_config.MONGO_PORT,
            my_config.MONGO_USER,
            my_config.MONGO_PASSWORD,
            my_config.MONGO_DATABASE,
        )

    def getAll(self):
        my_ticket = TicketUseCase(self.my_repository)
        data = my_ticket.getAll()

        return data

    def getByID(self, id):
        my_ticket = TicketUseCase(self.my_repository)
        datos = my_ticket.getByID(id)

        return datos

    def create(self, write_uid, ticket_id, description):
        my_dto = {
            "write_uid": write_uid,
            "ticket_id": ticket_id,
            "description": description,
        }
        my_ticket_struct = TicketInterface.fromDict(my_dto)
        my_ticket_use_case = TicketUseCase(self.my_repository)
        my_ticket = my_ticket_use_case.stateMachine(
            write_uid, TicketEvent.CREATED, my_ticket_struct
        )

        return my_ticket

    def update(self, write_uid, input_dict):
        my_dto = {k: v for k, v in input_dict if k in TicketStruct._fields}
        my_dto.update({"write_uid": write_uid})

        my_ticket_use_case = TicketUseCase(self.my_repository)
        my_ticket = my_ticket_use_case.stateMachine(
            write_uid, TicketEvent.UPDATED, my_dto
        )

        return my_ticket

    def delete(self, write_uid):
        my_ticket_use_case = TicketUseCase(self.my_repository)
        my_ticket = my_ticket_use_case.stateMachine(
            write_uid, TicketEvent.DELETED, {"write_uid": write_uid}
        )

        return my_ticket
