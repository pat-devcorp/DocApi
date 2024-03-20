from flask import Blueprint, request, send_from_directory
from werkzeug.utils import secure_filename

from ...domain.identifier_handler import IdentifierHandler
from ...utils.file_handler import FileHandler
from ..http_code import CODE_CREATED, FILE_NOT_PROVIDED

file_route = Blueprint("file", __name__)


@file_route.post("/")
def upload_file():
    # check if the post request has the file part
    if "file" not in request.files:
        code, message = FILE_NOT_PROVIDED
        return (code, message)
    file = request.files["file"]
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == "":
        code, message = FILE_NOT_PROVIDED
        return (code, message)
    code = IdentifierHandler.get_uuid_v4()
    filename = secure_filename(code)
    FileHandler(file_route.config["IMAGE_FOLDER"], filename)
    code, _ = CODE_CREATED
    return (code, filename)


@file_route.get("/uploads/<name>")
def download_file(name):
    return send_from_directory(file_route.config["IMAGE_FOLDER"], name)
