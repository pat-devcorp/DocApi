import mimetypes
import os

import magic
import requests

from ..infrastructure.config import Config
from .HandlerError import HandlerError
from .ResponseHandler import NOT_FOUND, UNSUPPORTED_MEDIA_TYPE, WARNING_FILE


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
    if my_config.VIRUS_ANALYZER_API is not None:
        is_ok = requests.post(my_config.VIRUS_ANALYZER_API, files=file)
        if is_ok != 200:
            raise HandlerError(WARNING_FILE)


class FileHanlder:
    file_id = None

    def __init__(self) -> None:
        my_config = Config()
        self.current_path = my_config.MEDIA_PATH

    def uploadFile(self, uploaded_file, name=None, directory: str = None) -> bool:
        isValidType(uploaded_file.stream)
        isSafe(uploaded_file)

        file_name = name or uploaded_file.filename
        if directory is not None and directory != "":
            self.current_path = os.path.join(self.current_path, directory)

        file_path = os.path.join(self.current_path, file_name)
        uploaded_file.save(file_path)

        self.file_id = file_path
        return True

    def fileExists(self, file_name: str, directory: str = None) -> bool:
        if directory is not None and directory != "":
            self.current_path = os.path.join(self.current_path, directory)

        file_path = os.path.join(self.current_path, file_name)
        if not os.path.exists(file_path):
            raise HandlerError(NOT_FOUND)

        self.file_id = file_path
        return True
