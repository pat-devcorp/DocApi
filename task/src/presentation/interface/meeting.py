from collections import namedtuple

from ...utils.DatetimeHandler import valdiateDatetimeFormat


MeetingDTO = namedtuple("MeetingDTO", ["meeting_date"])

class Meeting:
    @classmethod
    def create(meeting_date):
        valdiateDatetimeFormat(meeting_date)
        return MeetingDTO(meeting_date)
    
    @classmethod
    def getIdentifier(identifier):
        return AuditHandler.getIdentifier(identifier)