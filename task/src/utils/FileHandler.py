import mimetypes
import os
import subprocess

import magic
import requests

from ..infraestructure.config import Config
from ..utils.ErrorHandler import NOT_FOUND, UNSUPPORTED_MEDIA_TYPE, WARNING_FILE
from ..utils.HandlerError import HandlerError


def isValidType(file):
    my_config = Config()

    mime_type, _ = mimetypes.guess_type(file)
    if mime_type not in my_config.ALLOWED_EXTENSIONS:
        raise HandlerError(UNSUPPORTED_MEDIA_TYPE)

    my_magic = magic.Magic()
    file_type = my_magic.from_buffer(file.read(1024))
    my_magic.close()
    if file_type not in my_config.ALLOWED_EXTENSIONS:
        raise HandlerError(UNSUPPORTED_MEDIA_TYPE)

    return True


def isSafe(file) -> str:
    my_config = Config()
    if my_config.VIRUS_ANALIZER_API is not None:
        is_ok = requests.post(my_config.VIRUS_ANALIZER_API, files=file)
        if is_ok != 200:
            raise HandlerError(WARNING_FILE)


class FileHanlder:
    file_id = None

    def __init__(self) -> None:
        my_config = Config()
        _path = my_config.MEDIA_PATH

    def uploadFile(self, uploaded_file, name=None, directory: str = None) -> bool:
        isValidType(uploaded_file.stream)
        isSafe(uploaded_file)

        file_name = name or uploaded_file.filename
        file_path = self._path
        if directory is not None and directory != "":
            file_path = os.path.join(self.path, directory)

        uploaded_file.save(os.path.join(file_path, file_name))
        file_path = os.path.join(file_path, file_name)
        self.file_id = file_path
        return True

    def fileExists(self, file_name: str, directory: str = None) -> bool:
        file_path = self._path
        if directory is not None and directory != "":
            file_path = os.path.join(self.path, directory)
        file_path = os.path.join(file_path, file_name)

        if not os.path.exists(file_path):
            raise HandlerError(NOT_FOUND)
        self.file_id = file_path
        return True
