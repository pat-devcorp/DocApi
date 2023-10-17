from collections import namedtuple


KeywordStruct = namedtuple("keyword", ["keyword_id", "description"])
KeywordTicketStruct = namedtuple("keyword_ticket", ["keyword_id", "ticket_id"])