from flask import Blueprint, request

from ..ExceptionHandler import exception_handler
from ..status_code import REQUIRED_FIELD, WRITER_NOT_PROVIDED
from .src.presentation.controller.image import ImageController

image_route = Blueprint("image_route", __name__, url_prefix="/image")


@image_route.post("/")
@exception_handler
def create_image():
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)

    lc = ImageController(
        write_uid,
        image_route.config["IMAGE_PATH"],
        image_route.config["REPOSITORY_MONGO"],
        image_route.config["BROKER_RABBITMQ"],
    )
    item = lc.create(
        params.get("image_id"),
    )

    return (200, item)


@image_route.get("/", defaults={"id": None})
@image_route.get("/<id>")
@exception_handler
def fetch_images(id=None):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return code, message

    lc = ImageController(
        write_uid,
        image_route.config["IMAGE_PATH"],
        image_route.config["REPOSITORY_MONGO"],
        image_route.config["BROKER_RABBITMQ"],
    )
    data = lc.get_by_id(id) if id is not None else lc.fetch()

    return (200, data)


@image_route.put("/<id>")
@exception_handler
def update_image(id):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (image_id := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = ImageController(
        write_uid,
        image_route.config["IMAGE_PATH"],
        image_route.config["REPOSITORY_MONGO"],
        image_route.config["BROKER_RABBITMQ"],
    )
    item = lc.update(image_id, params)

    return (200, item)


@image_route.delete("/<id>")
@exception_handler
def delete_image(id):
    params = request.args.to_dict()

    if (write_uid := params.get("write_uid")) is None:
        code, message = WRITER_NOT_PROVIDED
        return (code, message)
    if (image_id := id) is None:
        code, message = REQUIRED_FIELD
        return (code, message)

    lc = ImageController(
        write_uid,
        image_route.config["IMAGE_PATH"],
        image_route.config["REPOSITORY_MONGO"],
        image_route.config["BROKER_RABBITMQ"],
    )
    item = lc.delete(image_id)

    return (200, item)
