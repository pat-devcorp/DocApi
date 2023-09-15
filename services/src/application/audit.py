from ..domain.audit import Audit as AuditDomain
from .repositoryProtocol import RepositoryProtocol


class Audit:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self.__fields__ = AuditDomain.__fields__

    def set_fields(self, fields: list):
        self.__fields__ = [field for field in fields if field in AuditDomain.__fields__]

    def get_all(self):
        return self.my_repository.get(AuditDomain.__tablename__, self.__fields__)

    def create(self, ref_dto):
        my_domain = AuditDomain.from_dict(ref_dto)

        self.my_repository.create(AuditDomain.__tablename__, my_domain.as_dict())

        return my_domain.as_dict()

    def get_by_id(self, value):
        return self.my_repository.get_by_id(
            AuditDomain.__tablename__, "_id", value, self.__fields__
        )

    def update(self, ref_dto):
        data = self.get_by_id(ref_dto._id)
        my_domain = AuditDomain.from_dict(data)
        my_domain.update()

        self.my_repository.update(
            AuditDomain.__tablename__, "_id", str(ref_dto._id), my_domain.as_dict()
        )

        return my_domain.as_dict()
