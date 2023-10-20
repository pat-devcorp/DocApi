from collections import namedtuple


Keyword = namedtuple("keyword", ["keyword_id", "description"])
KeywordTicket = namedtuple("keyword_ticket", ["keyword_id", "ticket_id"])

CheckList = namedtuple("checklist", ["checklist_id", "state", "description"])
CheckListTicket = namedtuple("checklist_ticket", ["checklist_id", "ticket_id"])

Meeting = namedtuple("meeting", ["meeting_id", "start_date"])
MeetingTicket = namedtuple("meeting_ticket", ["meeting_id", "ticket_id"])

TicketMembers = namedtuple("keyboard_ticket", ["user_id", "ticket_id"])
