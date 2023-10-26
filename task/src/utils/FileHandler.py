import mimetypes
import os
import subprocess

import magic
import requests

from ..infraestructure.config import Config
from ..utils.HandlerError import HandlerError


def isValidType(file):
    my_config = Config()

    mime_type, _ = mimetypes.guess_type(file)
    if mime_type not in my_config.ALLOWED_EXTENSIONS:
        raise HandlerError(f"File type {file_type} is not supported")

    my_magic = magic.Magic()
    file_type = my_magic.from_buffer(file.read(1024))
    my_magic.close()
    if file_type not in my_config.ALLOWED_EXTENSIONS:
        raise HandlerError(f"File type {file_type} is not supported")

    return True


def isSafe(file) -> str:
    my_config = Config()
    if my_config.VIRUS_ANALIZER_API is not None:
        is_ok = requests.post(my_config.VIRUS_ANALIZER_API, files=file)
        if is_ok != 200:
            raise HandlerError(f"File could be a virus")


def uploadFile(uploaded_file, directory):
    isValidType(uploaded_file.stream)
    isSafe(uploaded_file)

    my_config = Config()
    uploaded_file.save(
        os.path.join(my_config.MEDIA_PATH, directory, uploaded_file.filename)
    )
    return True


def fileExists(file_name, directory) -> str:
    my_config = Config()
    file_path = os.path.join(my_config.MEDIA_PATH, directory, file_name)
    if not os.path.exists(file_path):
        raise HandlerError(f"The file at {file_name} does not exist.")
    return file_path
