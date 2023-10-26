from collections import namedtuple

MemberDTO = namedtuple("MemberDTO", ["member_id", "role_id"])


class Member:
    @classmethod
    def create(member_id, role_id):
        role_identifier = MemberDomain.ensureRole(role_id)
        member_identifier = AuditHandler.getIdentifier(member_id)
        return MemberDTO(member_identifier, role_identifier)

    @classmethod
    def getIdentifier(identifier):
        return AuditHandler.getIdentifier(identifier)
