from ..struct.audit import Audit as AuditStruct
from .repositoryProtocol import RepositoryProtocol


class Audit:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self.__fields__ = AuditStruct.__fields__

    # def update(self, write_uid):
    #     self.write_uid = write_uid
    #     self.write_at = datetime.now()

    # def deactivate(self, write_uid):
    #     self.is_active = False
    #     self.update(write_uid)

    def setFields(self, fields: list):
        self.__fields__ = [field for field in fields if field in AuditStruct.__fields__]

    def getAll(self):
        return self.my_repository.get(AuditStruct.__tablename__, self.__fields__)
    
    def getByID(self, value):
        return self.my_repository.getByID(
            AuditStruct.__tablename__, "_id", value, self.__fields__
        )

    def create(self, ref_dto):
        my_audit_struct = AuditStruct.fromDict(ref_dto)

        self.my_repository.create(AuditStruct.__tablename__, my_audit_struct.asDict())

        return my_audit_struct.asDict()

    def update(self, ref_dto):
        data = self.getByID(ref_dto._id)
        my_audit_struct = AuditStruct.fromDict(data)
        my_audit_struct.update()

        self.my_repository.update(
            AuditStruct.__tablename__, "_id", str(ref_dto._id), my_audit_struct.asDict()
        )

        return my_audit_struct.asDict()
