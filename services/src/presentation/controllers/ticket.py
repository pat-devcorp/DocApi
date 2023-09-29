from ...application.ticket import Ticket as TicketUseCase
from ...struct.ticket import Ticket as TicketStruct
from ...infraestructure.config import Config
from ...infraestructure.repositories.mongo import Mongo as MongoRepository
from .controllerError import controllerError


class Ticket:
    my_repository = None

    def __init__(self, ref_repository=None):
        self.my_repository = (
            self.setRepository() if ref_repository is None else ref_repository
        )

    # TODO: remove?
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

    def create(self, write_uid, description: str):
        my_dto = {"write_uid": write_uid, "description": description}
        has_error = TicketStruct.ensure_description(description)
        if has_error:
            controllerError("VALIDATION", has_error)

        my_ticket = TicketUseCase(self.my_repository)
        my_obj = my_ticket.create(my_dto)

        return my_obj

    def update(self, write_uid, input_dict):
        my_dto = {k: v for k, v in input_dict if k in TicketStruct.__fields__}
        my_dto.update({"write_uid": write_uid})
        has_error = TicketStruct.validate(my_dto)
        if has_error:
            controllerError("VALIDATION", has_error)

        my_ticket = TicketUseCase(self.my_repository)
        my_obj = my_ticket.update(my_dto)

        return my_obj
