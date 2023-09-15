from ...application.ticket import Ticket as TicketUseCase
from ...domain.ticket import Ticket as TicketDomain
from ...infraestructure.config import Config
from ...infraestructure.repositories.mongo import Mongo as MongoRepository
from .controllerError import controllerError


class Ticket:
    my_repository = None

    def __init__(self, ref_repository=None):
        self.my_repository = (
            self.set_repository() if ref_repository is None else ref_repository
        )

    def set_repository(self):
        my_config = Config()
        self.my_repository = MongoRepository(
            my_config.MONGO_HOST,
            my_config.MONGO_PORT,
            my_config.MONGO_USER,
            my_config.MONGO_PASSWORD,
            my_config.MONGO_DATABASE,
        )

    def get_all(self):
        my_ticket = TicketUseCase(self.my_repository)
        data = my_ticket.get_all()
        return data

    def get_by_id(self, id: str):
        my_ticket = TicketUseCase(self.my_repository)
        datos = my_ticket.get_by_id(id)
        return datos

    def create(self, write_uid, description: str):
        my_dto = {"write_uid": write_uid, "description": description}
        has_error = TicketDomain.ensure_description(description)
        if has_error:
            controllerError("VALIDATION", has_error)

        my_ticket = TicketUseCase(self.my_repository)
        my_obj = my_ticket.create(my_dto)

        return my_obj

    def update(self, write_uid, input_dict):
        my_dto = {k: v for k, v in input_dict if k in TicketDomain.__fields__}
        my_dto.update({"write_uid": write_uid})
        has_error = TicketDomain.validate_schema(my_dto)
        if has_error:
            controllerError("VALIDATION", has_error)

        my_ticket = TicketUseCase(self.my_repository)
        my_obj = my_ticket.update(my_dto)

        return my_obj
