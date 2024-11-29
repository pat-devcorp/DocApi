import logging

from flask import Blueprint, current_app, request

logger = logging.getLogger(__name__)

from src.presentation.controller.task import TaskController

from .exception_handler import exception_handler
from .status_code import REQUIRED_FIELD, WRITER_NOT_PROVIDED

task_route = Blueprint("task_route", __name__)


@task_route.post("/task")
@exception_handler
def create_task():
    params = request.get_json()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)

    lc = TaskController(
        writeUId,
        current_app.myApp.MyMongo,
        current_app.myApp.MyRabbitmq,
    )

    _ = lc.create(
        params.get("taskId"),
        params.get("requirement"),
        params.get("milestones"),
        params.get("because"),
        TaskController.setState(params.get("state")),
    )

    return "OK"


@task_route.get("/task", defaults={"identifier": None})
@task_route.get("/task/<identifier>")
@exception_handler
def fetch_tasks(identifier=None):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return code, message

    lc = TaskController(
        writeUId,
        current_app.myApp.MyMongo,
        current_app.myApp.MyRabbitmq,
    )
    data = lc.get_by_id(identifier) if identifier is not None else lc.fetch()

    return data


@task_route.put("/task/<identifier>")
@exception_handler
def update_task(identifier):
    params = request.get_json()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (taskId := identifier) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = TaskController(
        writeUId,
        current_app.myApp.MyMongo,
        current_app.myApp.MyRabbitmq,
    )
    _ = lc.update(taskId, params)

    return "OK"


@task_route.delete("/task/<identifier>")
@exception_handler
def delete_task(identifier):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (taskId := identifier) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = TaskController(
        writeUId,
        current_app.myApp.MyMongo,
        current_app.myApp.MyRabbitmq,
    )
    _ = lc.delete(taskId)

    return "OK"
