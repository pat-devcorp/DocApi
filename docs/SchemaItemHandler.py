from enum import Enum

from pydantic import BaseModel


class SchemaItemHandler(BaseModel):
    requiredInCreate: bool
    isEditable: bool
    valueType: str
    default: any
    values: dict | list

    def __init__(
        self, requiredInCreate, isEditable, valueType, default=None, values=[]
    ):
        self.requiredInCreate = requiredInCreate
        self.isEditable = isEditable
        self.valueType = valueType
        self.default = default
        if isinstance(values, Enum):
            self.values = {i.name: i.value for i in values}
        else:
            self.values = values
