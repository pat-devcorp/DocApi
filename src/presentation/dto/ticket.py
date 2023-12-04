from ...domain.dao.ticket import (
    TicketCategory,
    TicketDAO,
    TicketState,
    TicketTypeCommit,
    ValidTicket,
)
from ...utils.ResponseHandler import ID_NOT_FOUND, PRESENTATION_VALIDATION
from ..IdentifierHandler import IdentifierHandler
from ..PresentationError import PresentationError


class TicketDTO:
    ticket_id: IdentifierHandler
    description: str
    category: TicketCategory
    type_commit: TicketTypeCommit
    state: TicketState

    @staticmethod
    def getFields():
        return ["ticket_id", "description", "category", "type_commit", "state"]

    @classmethod
    def getMock(cls):
        identity = cls.getIdentifier("873788d4-894c-11ee-b9d1-0242ac120002")
        return cls(ticket_id=identity, description="Test task")

    def asDict(self):
        data = dict()

        data["description"] = self.description if self.description is not None else None

        data["tiket_id"] = self.ticket_id.value if self.ticket_id is not None else None
        data["category"] = self.category.value if self.category is not None else None
        data["type_commit"] = (
            self.type_commit.value if self.type_commit is not None else None
        )
        data["state"] = self.state.value if self.state is not None else None

        return data

    @staticmethod
    def filterKeys(data: dict):
        return {k: v for k, v in data.items() if k in TicketDTO.getFields()}

    @staticmethod
    def getIdentifier(ticket_id):
        pk = IdentifierHandler(TicketDAO.getIdAlgorithm())
        pk.setIdentifier(ticket_id)
        return pk

    @classmethod
    def fromDict(cls, params: dict) -> None | PresentationError:
        data = {k: params.get(k, None) for k in cls.getFields()}

        if (tiket_id := data.get("tiket_id")) is None:
            raise PresentationError(ID_NOT_FOUND, "tiket_id is not present")
        data["tiket_id"] = cls.getIdentifier(tiket_id)

        if (category := data.get("category")) is not None:
            data["category"] = TicketCategory(category)

        if (type_commit := data.get("type_commit")) is not None:
            data["type_commit"] = TicketTypeCommit(type_commit)

        if (state := data.get("state")) is not None:
            data["state"] = TicketState(state)

        return cls(**data)

    def __init__(
        self,
        ticket_id: IdentifierHandler,
        description: str,
        category: int = TicketCategory.UNDEFINED.value,
        type_commit: int = TicketTypeCommit.UNDEFINED.value,
        state: int = TicketState.CREATED.value,
    ) -> None | PresentationError:
        data = {
            "ticket_id": ticket_id,
            "description": description,
            "category": category,
            "type_commit": type_commit,
            "state": state,
        }
        is_ok, err = ValidTicket.isValid(data, False)
        if not is_ok:
            raise PresentationError(PRESENTATION_VALIDATION, "\n".join(err))

        self.ticket_id = ticket_id
        self.description = description
        self.category = TicketCategory(category)
        self.type_commit = TicketTypeCommit(type_commit)
        self.state = TicketState(state)
