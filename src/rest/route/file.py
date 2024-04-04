from flask import Blueprint, send_from_directory

file_route = Blueprint("file_route", __name__)


@file_route.get("/uploads/<name>")
def download_file(name):
    return send_from_directory(file_route.config["IMAGE_PATH"], name)
