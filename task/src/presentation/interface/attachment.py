from collections import namedtuple

from ...utils.FileHandler import uploadFile

AttachmentDTO = namedtuple('AttachmentDTO', ["name", "path"])

class Attachment:
    @classmethod
    def create(attachment, directory):
        attachment_path = uploadFile(attachment, directory)
        return AttachmentDTO(attachment.name, attachment_path)
    
    @classmethod
    def getIdentifier(identifier):
        return AuditHandler.getIdentifier(identifier)