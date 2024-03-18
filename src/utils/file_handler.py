import mimetypes
import os

import magic
import requests

from .HandlerError import HandlerError
from .response_code import NOT_FOUND, UNSUPPORTED_MEDIA_TYPE, WARNING_FILE

ALLOWED_EXTENSIONS = ["pdf"]
VIRUS_ANALYZER_API = "https://www.virustotal.com/gui/home/upload"


def is_valid_type(file, allowed_extensions=ALLOWED_EXTENSIONS):
    mime_type, _ = mimetypes.guess_type(file)
    if mime_type not in allowed_extensions:
        raise HandlerError(UNSUPPORTED_MEDIA_TYPE)

    my_magic = magic.Magic()
    file_type = my_magic.from_buffer(file.read(1024))
    my_magic.close()
    if file_type not in allowed_extensions:
        raise HandlerError(UNSUPPORTED_MEDIA_TYPE)

    return True


def is_safe(file, virus_api=VIRUS_ANALYZER_API) -> str:
    if virus_api is not None:
        is_ok = requests.post(virus_api, files=file)
        if is_ok != 200:
            raise HandlerError(WARNING_FILE)


class FileHanlder:
    file_id = None

    def __init__(self, media_path) -> None:
        self.current_path = media_path

    def upload_file(self, uploaded_file, name=None, directory: str = None) -> bool:
        is_valid_type(uploaded_file.stream)
        is_safe(uploaded_file)

        file_name = name or uploaded_file.filename
        if directory is not None and directory != "":
            self.current_path = os.path.join(self.current_path, directory)

        file_path = os.path.join(self.current_path, file_name)
        uploaded_file.save(file_path)

        self.file_id = file_path
        return True

    def file_exists(self, file_name: str, directory: str = None) -> bool:
        if directory is not None and directory != "":
            self.current_path = os.path.join(self.current_path, directory)

        file_path = os.path.join(self.current_path, file_name)
        if not os.path.exists(file_path):
            raise HandlerError(NOT_FOUND)

        self.file_id = file_path
        return True
