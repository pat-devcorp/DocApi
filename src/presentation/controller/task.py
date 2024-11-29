from typing import List

from ...application.use_case.task import TaskUseCase
from ...domain.enum.task_channel_type import TaskChannelType
from ...domain.enum.task_state import TaskState
from ...domain.model.task import TaskDomain
from ...infrastructure.my_mongo.repositories.task_mongo import TaskMongo
#TODO:fix
#delete this class add mapper and model in route

class TaskController:
    def __init__(
        self,
        refWriteUId,
        refRepository,
        refBroker,
    ) -> None:
        self._r = TaskMongo(refRepository)
        self._uc = TaskUseCase(refWriteUId, self._r, refBroker)

    def fetch(self) -> list:
        return self._uc.fetch(0)

    def get_by_id(self, identifier: str):
        return self._uc.get_by_id(identifier)

    def delete(self, identifier: str):
        return self._uc.delete(identifier)

    def update(self, identifier: str, params: dict):
        obj = TaskDomain.from_dict(identifier, params)
        return self._uc.update(obj)

    def create(
        self,
        taskId: str,
        requirement: str,
        milestones: List[str],
        because: str,
        state: TaskState,
    ):
        obj = TaskDomain.new(taskId, requirement, milestones, because, state)

        return self._uc.create(obj)

    @staticmethod
    def setState(state):
        return TaskState.CREATED if state is not None else TaskState(state)
