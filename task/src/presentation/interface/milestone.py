from collections import namedtuple

from .InterfaceError import InterfaceError

MilestoneItemDTO = namedtuple(
    "MilestoneItemsDTO", ["milestone_id", "description", "state"]
)
MilestoneDTO = namedtuple("MilestoneDTO", ["milestone_id", "name", "items"])


class Milestone:
    @classmethod
    def getIdentifier(identifier):
        return MilestoneDomain.getIdentifier(identifier)

    @classmethod
    def fromDict(cls, params):
        ticket_dto = dict()
        for k in MilestoneDTO._fields:
            ticket_dto[k] = params[k] if params.get(k) is not None else None

    @classmethod
    def create(name, items):
        milestone_items = list()
        for item in items:
            milestone_items.append(MilestoneItem(item))
        return MilestoneDTO(name, items)


class MilestoneItem:
    @classmethod
    def fromDict(cls, params):
        ticket_dto = dict()
        for k in MilestoneItemDTO._fields:
            ticket_dto[k] = params[k] if params.get(k) is not None else None

    @classmethod
    def create(cls, description, is_check=False):
        return MilestoneItemDTO(description, is_check=is_check)
