# Create module Task

## Description

**I:** Patrick Alonso Fuentes Carpio

**AS:** A developer, I need a task module.

**I WANT TO:** Create a new task, associate users with different roles to the task, add meetings, link related words to the task for searching, conduct surveys, and maintain a list of milestones related to the task.

**BECAUSE**: I want to enhance traceability and provide accurate statistics.

**MILESTONES:**
- Create, edit, and delete tasks.
- Add team members.
- Send notifications to team members based on task-related events.
- Create surveys.
- Schedule meetings.
- Associate keywords with the task for searching.
- Generate a task document.

**NOTES:** The module should be developed following clean architecture principles.

## Milestones

1.

## Not covered

## Members

**AS A:** **ASSIGNEE** Patrick Alonso Fuentes Carpio

## Meetings

**SUBEJECT:** Defining the task
**DATE:** 03/10/2023 16:30

## Ballots

**SUBJECT:** Aprobe of the task
**VOTES YES:** 
- Patrick Alonso Fuentes Carpio
**VOTES NO:**

Keyword = namedtuple("keyword", ["keyword_id", "description"])
TicketKeywords = namedtuple("ticket_keyword", ["keyword_id", "ticket_id"])

Checklist = namedtuple("checklist", ["checklist_id", "description"])
ChecklistItem = namedtuple(
    "checklist_item", ["checklist_id", "checklist_item_id", "is_check", "description"]
)
TicketChecklist = namedtuple("ticket_checklist", ["checklist_id", "ticket_id"])

Meeting = namedtuple("meeting", ["meeting_id", "subject", "start_date"])
TicketMeetings = namedtuple("ticket_meeting", ["meeting_id", "ticket_id"])

Attachment = namedtuple("attachment", ["attachment_id", "path", "description"])
TicketAttachments = namedtuple("ticket_attachment", ["attachment_id", "ticket_id"])

Ballot = namedtuple("ballot", ["ballot_id", "description"])
BallotVote = namedtuple("vote", ["ballot_id", "vote_id", "member_id"])
TicketBallots = namedtuple("ticket_ballot", ["ticket_id", "ballot_id"])

TicketRole = namedtuple(
    "ticket_role",
    ["ticket_role_id", "description", "has_read_acccess", "has_write_acccess"],
)
TicketMembers = namedtuple("ticket_keyboard", ["user_id", "ticket_id", "role_id"])
TicketAssignees = namedtuple(
    "ticket_assignee",
    ["ticket_id", "estimate_time_in_minutes", "end_at", "earn_points"],
)