from ..struct.audit import Audit as AuditDomain
from ..struct.audit import AuditStruct
from .repositoryProtocol import RepositoryProtocol


class Audit:
    my_repository = None

    def __init__(self, ref_repository: RepositoryProtocol):
        self.my_repository = ref_repository
        self._fields = AuditStruct._fields

    # def update(self, write_uid):
    #     self.write_uid = write_uid
    #     self.write_at = datetime.now()

    # def deactivate(self, write_uid):
    #     self.is_active = False
    #     self.update(write_uid)

    def setFields(self, fields: list):
        self._fields = [field for field in fields if field in AuditStruct._fields]

    def getAll(self):
        return self.my_repository.get(AuditStruct.__name__, self._fields)
    
    def getByID(self, value):
        return self.my_repository.getByID(
            AuditStruct.__name__, "_id", value, self._fields
        )

    def create(self, ref_dto):
        my_audit_struct = AuditDomain.fromDict(ref_dto)

        self.my_repository.create(AuditStruct.__name__, my_audit_struct.asDict())

        return my_audit_struct.asDict()

    def update(self, ref_dto):
        data = self.getByID(ref_dto._id)
        my_audit_struct = AuditDomain.fromDict(data)
        my_audit_struct.update()

        self.my_repository.update(
            AuditStruct.__name__, "_id", str(ref_dto._id), my_audit_struct.asDict()
        )

        return my_audit_struct.asDict()
