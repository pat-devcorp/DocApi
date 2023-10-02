from ...application.ticket import Ticket as TicketUseCase
from ...infraestructure.config import Config
from ...infraestructure.repositories.mongo import Mongo as MongoRepository
from ...struct.ticket import EventTicket
from ...struct.ticket import Ticket as TicketDomain
from ...struct.ticket import TicketStruct
from .ControllerError import controllerError


class Ticket:
    my_repository = None

    def __init__(self, ref_repository=None):
        self.my_repository = (
            self.setRepository() if ref_repository is None else ref_repository
        )

    def setRepository(self):
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

    def getByID(self, id: str):
        my_ticket = TicketUseCase(self.my_repository)
        datos = my_ticket.getByID(id)

        return datos

    def create(self, write_uid, ticket_id, description: str):
        errors = list()

        my_identity_error = TicketDomain.ensureTicketId(ticket_id)
        if my_identity_error is not None:
            errors.append("\nIdentity not valid for ticket")

        description_error = TicketDomain.ensureDescription(description)
        if len(description_error) > 0:
            errors.append("\nDescription not valid for ticket")

        if errors:
            controllerError(errors)

        my_dto = {
            "write_uid": write_uid,
            "ticket_id": ticket_id,
            "description": description,
        }
        my_ticket_use_case = TicketUseCase(self.my_repository)
        my_ticket = my_ticket_use_case.stateMachine(EventTicket.CREATED, my_dto)

        return my_ticket

    def update(self, write_uid, input_dict):
        my_dto = {k: v for k, v in input_dict if k in TicketStruct._fields}
        my_dto.update({"write_uid": write_uid})

        my_ticket_use_case = TicketUseCase(self.my_repository)
        my_ticket = my_ticket_use_case.stateMachine(EventTicket.UPDATED, my_dto)

        return my_ticket

    def delete(self, write_uid):
        my_ticket_use_case = TicketUseCase(self.my_repository)
        my_ticket = my_ticket_use_case.stateMachine(
            EventTicket.DELETED, {"write_uid": write_uid}
        )

        return my_ticket
