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
    ticketId: IdentifierHandler
    description: str
    category: TicketCategory
    typeCommit: TicketTypeCommit
    state: TicketState

    @staticmethod
    def getFields():
        return ["ticketId", "description", "category", "typeCommit", "state"]

    @classmethod
    def getMock(cls):
        identity = cls.getIdentifier("873788d4-894c-11ee-b9d1-0242ac120002")
        return cls(ticketId=identity, description="Test task")

    def asDict(self):
        data = dict()

        data["description"] = self.description if self.description is not None else None

        data["ticketId"] = self.ticketId.value if self.ticketId is not None else None
        data["category"] = self.category.value if self.category is not None else None
        data["typeCommit"] = (
            self.typeCommit.value if self.typeCommit is not None else None
        )
        data["state"] = self.state.value if self.state is not None else None

        return data

    @staticmethod
    def filterKeys(data: dict):
        return {k: v for k, v in data.items() if k in TicketDTO.getFields()}

    @staticmethod
    def getIdentifier(ticketId):
        pk = IdentifierHandler(TicketDAO.getIdAlgorithm())
        pk.setIdentifier(ticketId)
        return pk

    @classmethod
    def fromDict(cls, params: dict) -> None | PresentationError:
        data = {k: params.get(k, None) for k in cls.getFields()}

        if (ticketId := data.get("ticketId")) is None:
            raise PresentationError(ID_NOT_FOUND, "ticketId is not present")
        data["ticketId"] = cls.getIdentifier(ticketId)

        if (category := data.get("category")) is not None:
            data["category"] = TicketCategory(category)

        if (typeCommit := data.get("typeCommit")) is not None:
            data["typeCommit"] = TicketTypeCommit(typeCommit)

        if (state := data.get("state")) is not None:
            data["state"] = TicketState(state)

        return cls(**data)

    def __init__(
        self,
        ticketId: IdentifierHandler,
        description: str,
        category: int = TicketCategory.UNDEFINED.value,
        typeCommit: int = TicketTypeCommit.UNDEFINED.value,
        state: int = TicketState.CREATED.value,
    ) -> None | PresentationError:
        data = {
            "ticketId": ticketId,
            "description": description,
            "category": category,
            "typeCommit": typeCommit,
            "state": state,
        }
        is_ok, err = ValidTicket.isValid(data, False)
        if not is_ok:
            raise PresentationError(PRESENTATION_VALIDATION, "\n".join(err))

        self.ticketId = ticketId
        self.description = description
        self.category = TicketCategory(category)
        self.typeCommit = TicketTypeCommit(typeCommit)
        self.state = TicketState(state)
