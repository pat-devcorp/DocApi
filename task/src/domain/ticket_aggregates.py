from collections import namedtuple


Keyword = namedtuple("keyword", ["keyword_id", "description"])
TicketKeywords = namedtuple("ticket_keyword", ["keyword_id", "ticket_id"])

Checklist = namedtuple("checklist", ["checklist_id", "description"])
ChecklistItem = namedtuple("checklist_item", ["checklist_id", "checklist_item_id", "is_check", "description"])
TicketChecklist = namedtuple("ticket_checklist", ["checklist_id", "ticket_id"])

Meeting = namedtuple("meeting", ["meeting_id", "subject", "start_date"])
TicketMeetings = namedtuple("ticket_meeting", ["meeting_id", "ticket_id"])

Attachment = namedtuple("attachment", ["attachment_id", "path", "description"])
TicketAttachments = namedtuple("ticket_attachment", ["attachment_id","ticket_id"])

Ballot = namedtuple("ballot", ["ballot_id", "description"])
BallotVote = namedtuple("vote", ["ballot_id", "vote_id", "member_id"])
TicketBallots = namedtuple("ticket_ballot", ["ticket_id", "ballot_id"])

TicketRole = namedtuple("ticket_role", ["ticket_role_id", "description", "has_read_acccess", "has_write_acccess"])
TicketMembers = namedtuple("ticket_keyboard", ["user_id", "ticket_id", "role_id"])
TicketAssignees = namedtuple("ticket_assignee", ["ticket_id", "estimate_time_in_minutes", "end_at", "earn_points"])