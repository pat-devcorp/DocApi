from ..custom_enum import CustomEnum


class TicketEvent(CustomEnum):
    CREATED = 0
    UPDATED = 1
    DELETED = 2
    ADD_MEMBER = 3
