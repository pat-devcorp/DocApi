from pydantic import BaseModel


class SchemaItemHandler:
    requiredInCreate: bool
    isEditable: bool
    valueType: str
    default
    values

    def __init__(
        self,
        requiredInCreate
        isEditable
        valueType
        default = None
        values = {}
    ):
        self.requiredInCreate = requiredInCreate
        self.isEditable = isEditable
        self.valueType = valueType
        self.default = default
        if isintance(values, Enum):
            self.values = {i.name: i.value for i in TicketCategory}
        else:
            self.values = values