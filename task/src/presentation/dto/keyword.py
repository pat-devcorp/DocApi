import re
from collections import namedtuple

from ...utils.StringHandler import contains_only_letters
from ..PresentationError import PresentationError

KeywordDTO = namedtuple("KeywordDTO", ["keyword"])


class KeywordHandler:
    @classmethod
    def isValid(keyword):
        error = list()
        if keyword is None:
            error += "Empty string"
        if len(keyword) > 30:
            error += "Too many characters"
        if not re.match(r"^[a-zA-Z0-9_-]+$", keyword):
            error += "Invalid keyword"
        if not contains_only_letters(keyword):
            error += "Symbools is not supported"
        if len(error) > 0:
            PresentationError(
                "Invalid keyword: %s for this reasons: %s"
                % (keyword, "\n".joint(error))
            )

    @classmethod
    def create(attachment):
        return KeywordDTO(attachment.name, attachment.path)

    @classmethod
    def getIdentifier(identifier):
        return KeywordDomain.getIdentifier(identifier)
