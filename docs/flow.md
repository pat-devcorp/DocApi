```mermaid
classDiagram
JSON --> TicketDTO :toDict
TicketDTO --> TicketController
class TicketDTO{
    str, description, Test task,
    TicketCategory, category, TicketCategory.UNDEFINED,
    TicketTypeCommit, typeCommit, TicketTypeCommit.UNDEFINED,
    TicketState, state, TicketState.CREATED,
}
```