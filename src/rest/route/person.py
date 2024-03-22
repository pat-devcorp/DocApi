from flask import Blueprint, request

from ...presentation.controller.person import PersonController
from ..ExceptionHandler import exception_handler
from ..http_code import REQUIRED_FIELD, WRITER_NOT_PROVIDED

person = Blueprint("person", __name__, url_prefix="/person")


@person.post("/")
@exception_handler
def create_person():
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)

    lc = PersonController(
        writeUId, person.config["MONGO_SERVER"], person.config["RABBITMQ_SERVER"]
    )
    item = lc.create(
        params.get("personId"),
        params.get("name"),
        params.get("lastName"),
        params.get("mailAddress"),
        params.get("birthDate"),
        params.get("documentNumber"),
        params.get("address"),
    )

    return (200, item)


@person.get("/", defaults={"id": None})
@person.get("/<id>")
@exception_handler
def fetch_persons(id=None):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return code, message

    lc = PersonController(
        writeUId, person.config["MONGO_SERVER"], person.config["RABBITMQ_SERVER"]
    )
    data = lc.get_by_id(id) if id is not None else lc.fetch()

    return (200, data)


@person.put("/<id>")
@exception_handler
def update_person(id):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (personId := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = PersonController(
        writeUId, person.config["MONGO_SERVER"], person.config["RABBITMQ_SERVER"]
    )
    item = lc.update(personId, params)

    return (200, item)


@person.delete("/<id>")
@exception_handler
def delete_person(id):
    params = request.args.to_dict()

    if (writeUId := params.get("writeUId")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (personId := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = PersonController(
        writeUId, person.config["MONGO_SERVER"], person.config["RABBITMQ_SERVER"]
    )
    item = lc.delete(personId)

    return (200, item)
