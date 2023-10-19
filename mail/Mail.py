import datetime
import email
import imaplib
import ntpath
import os
import platform
import smtplib
import sys
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Constants:
    """
    Wraps search criterias' constants for IMAP protocol
    """

    ALL = "ALL"
    ANSWERED = "ANSWERED"
    DELETED = "DELETED"
    FLAGGED = "FLAGGED"
    NEW = "NEW"
    OLD = "OLD"
    RECENT = "RECENT"
    SEEN = "SEEN"
    UNANSWERED = "UNANSWERED"
    UNDELETED = "UNDELETED"
    UNFLAGGED = "UNFLAGGED"
    UNKEYWORD = "UNKEYWORD"
    UNSEEN = "UNSEEN"

    # require string arg:
    BCC = "BBC"
    CC = "CC"
    BODY = "BODY"
    FROM = "FROM"
    KEYWORD = "KEYWORD"
    SUBJECT = "SUBJECT"
    TEXT = "TEXT"
    TO = "TO"

    # require date arg:
    ON = "ON"
    SINCE = "SINCE"
    BEFORE = "BEFORE"


class ServiceManager(object):
    _services = [
        {
            "id": "artatlas",
            "smtp_addr": "mail.artatlasperu.com",
            "smtp_port": 587,
            "smtp_ssl_port": 465,
            "imap_addr": "mail.artatlasperu.com",
            "imap_port": 143,
            "imap_ssl_port": 993,
        }
    ]

    def __init__(self, select: int = 0):
        try:
            service = self._services[select]
            self.id = service["id"]
            self.smtp_addr = service["smtp_addr"]
            self.smtp_port = service["smtp_port"]
            self.smtp_ssl_port = service.get("smtp_ssl_port")
            self.imap_addr = service["imap_addr"]
            self.imap_port = service["imap_port"]
            self.imap_ssl_port = service.get("imap_ssl_port")
        except Exception as e:
            print(f"Error while loading: {repr(e)}")


class EMessage:
    """
    Class wrapping major parts of a message
    """

    Body = None
    Attachments = None

    def __init__(self, fromAddr, toaddrs, subject, date):
        self.From = str(fromAddr)
        self.Subject = str(subject)
        self.Date = date
        self.To = toaddrs

    def __str__(self):
        return f"FROM:{self.From}\nSubject:{self.Subject}\nDate:{self.Date}\nTo:{self.To}"

class MailService(ServiceManager):
    """
    Class providing connection to email service, messages sending
    and reading
    """

    def __init__(self, user: str, password: str, service: ServiceManager, ssl: bool = False):
        self._user = user
        self._password = password
        self.ssl = ssl
        self.id = service.id
        self.smtp_addr = service.smtp_addr
        self.smtp_port = service.smtp_port
        self.smtp_ssl_port = service.smtp_ssl_port
        self.imap_addr = service.imap_addr
        self.imap_port = service.imap_port
        self.imap_ssl_port = service.imap_ssl_port

    def __enter__(self):
        self.imap = None
        self.smtp = None
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.imap.close()
            self.imap.logout()
        except AttributeError:
            pass
        try:
            self.smtp.close()
            self.smtp.logout()
        except AttributeError:
            pass

    @staticmethod
    def path_leaf(path):
        h, t = ntpath.split(path)
        return t or ntpath.basename(h)

    def send(self, toaddrs, subject, body="", attachments=None):
        try:
            msg = MIMEMultipart()
            msg["Subject"] = subject
            msg["From"] = self._user
            msg["To"] = ", ".join(toaddrs)

            body = MIMEText(body)
            msg.attach(body)

            if attachments is not None:
                for a in attachments:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(open(a, "rb").read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        ('attachment; filename="%s"' % MailService.path_leaf(a)),
                    )
                    msg.attach(part)

            self.smtp = smtplib.SMTP(self.smtp_addr, self.smtp_port)
            self.smtp.login(self._user, self._password)
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.sendmail(self._user, toaddrs, msg.as_string())
            return True

        except Exception as e:
            print(("Error while sending message: %s" % repr(e)))
            return False

    def read(self, limit_consulted=8, criteria="UNSEEN", download_attachments=False):
        print("---STARTING")
        i = 0
        while True:
            self.imap = (
                imaplib.IMAP4_SSL(self.imap_addr, self.imap_ssl_port)
                if self.ssl
                else imaplib.IMAP4(self.imap_addr, self.imap_port)
            )
            r, d = self.imap.login(self._user, self._password)
            assert r == "OK", "login failed"
            print("---TRYING TO READ")
            try:
                print("---SELECTING MESSAGES")
                self.imap.select()

                retval = []

                result, datos = self.imap.uid("search", None, criteria)
                if result == "OK":
                    print(datos)
                    for num in datos[0].split():
                        result, data = self.imap.uid("fetch", num, "(RFC822)")
                        print(result)
                        print(data)
                        if result == "OK":
                            if sys.version_info[0] < 3:
                                e_msg = email.message_from_string(data[0][1])
                            else:
                                e_msg = email.message_from_bytes(data[0][1])

                            # Date:
                            _date = None
                            date_t = email.utils.parsedate_tz(e_msg["Date"])
                            if date_t:
                                _date = datetime.datetime.fromtimestamp(
                                    email.utils.mktime_tz(date_t)
                                )

                            newEmsg = EMessage(
                                e_msg["From"], e_msg["To"], e_msg["Subject"], _date
                            )
                            newEmsg.Body = []

                            # content:
                            if e_msg.is_multipart():
                                for payload in e_msg.get_payload():
                                    newEmsg.Body.append(str(payload.get_payload()))
                            else:
                                newEmsg.Body.append(str(e_msg.get_payload()))

                            # attachments:
                            newEmsg.Attachments = []
                            for part in e_msg.walk():
                                # ignoring parts multi-part without attachments
                                if part.get_content_maintype() == "multipart":
                                    continue
                                if part.get("Content-Disposition") is None:
                                    continue

                                fileName = part.get_filename()

                                if fileName is not None:
                                    newEmsg.Attachments.append(str(fileName))

                                    if download_attachments:
                                        if platform.system() == "Windows":
                                            os.system(
                                                "if not exist attachments mkdir attachments"
                                            )
                                        else:
                                            os.system("mkdir -p ./attachments/")
                                        filePath = os.path.join(
                                            "./attachments/", fileName
                                        )
                                        if not os.path.isfile(filePath):
                                            fp = open(filePath, "wb")
                                            fp.write(part.get_payload(decode=True))
                                            fp.close()
                                            print("Downloaded attachment: " + filePath)
                                        else:
                                            print(
                                                ("File '%s' already exists" % filePath)
                                            )

                            retval.append(newEmsg)
                return retval
            except imaplib.IMAP4.abort as e:
                print(f"INTETO NUMERO {i}")
                print(e)
                if i > limit_consulted:
                    raise imaplib.IMAP4.abort("USAGE LIMIT EXCEEDED")
                i += 1
                continue


if __name__ == "__main__":
    service = ServiceManager()
    mail = MailService("patrickfuentes@artatlasperu.com", "$@7las$P3ru2023$", service)
    emails = mail.read()
    print("--MAILS--")
    print(emails)