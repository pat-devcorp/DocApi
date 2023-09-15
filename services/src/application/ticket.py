from ..domain.audit import Audit as AuditDomain
from ..domain.ticket import Ticket as TicketDomain
from .audit import Audit as AuditUseCase
from .repositoryProtocol import RepositoryProtocol


class Ticket:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self.__fields__ = TicketDomain.__fields__

    def set_fields(self, fields: list):
        self.__fields__ = [
            field for field in fields if field in TicketDomain.__fields__
        ]

    def get_all(self):
        return self.my_repository.get(TicketDomain.__tablename__, self.__fields__)

    def create(self, ref_dto: dict):
        my_dto = {k: v for k, v in ref_dto.items() if k in AuditDomain.__fields__}
        my_audit = AuditUseCase(self.my_repository)
        ref_audit = my_audit.create(my_dto)
        print(ref_audit)
        ref_dto.update({"audit": ref_audit._id})

        my_domain = TicketDomain.from_dict(ref_dto)
        my_domain.create()

        self.my_repository.create(self.__tablename__, my_domain.as_dict())

        return my_domain.as_dict()

    def get_by_id(self, value):
        return self.my_repository.get_by_id(
            TicketDomain.__tablename__, "_id", value, self.__fields__
        )

    def update(self, ref_dto: dict):
        my_dto = {k: v for k, v in ref_dto.items() if k in AuditDomain.__fields__}
        my_audit = AuditUseCase(self.my_repository)
        my_audit.update(my_dto)

        data = self.get_by_id(ref_dto._id)
        my_domain = TicketDomain.from_dict(data)
        my_domain.update()

        self.my_repository.update(
            TicketDomain.__tablename__, "_id", str(ref_dto._id), my_domain.as_dict()
        )

        return my_domain.as_dict()
