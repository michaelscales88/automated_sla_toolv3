import datetime

from src.CONSTANTS import (USER_NAME,
                           USER_NAME2,
                           PASSWORD,
                           PASSWORD2,
                           LOGIN_TYPE,
                           LOGIN_TYPE2,
                           ATTACH_DIR,
                           ATTACH_DIR2)
from src.download_attachment import download_attachments
from src.outlook import Outlook


def get_voice_mail(use_date):
    mail = Outlook(use_date, LOGIN_TYPE)
    mail.login(USER_NAME, PASSWORD)
    mail.inbox()
    read_ids = mail.read_ids()
    return mail.get_voice_mail_info(read_ids)


def get_attachments(use_date):
    mail = Outlook(use_date, LOGIN_TYPE2)
    mail.login(USER_NAME2, PASSWORD2)
    mail.inbox()
    read_ids = mail.read_ids()
    return mail.get_voice_mail_info(read_ids)


def get_downloads(use_date, download_type='Archive'):
    use_date = use_date + datetime.timedelta(days=1)
    print("Attachment download date is: %s" % use_date)
    if download_type == 'Archive':
        download_attachments(use_date, LOGIN_TYPE2, USER_NAME2, PASSWORD2, ATTACH_DIR)
    else:
        download_attachments(use_date, LOGIN_TYPE2, USER_NAME2, PASSWORD2, ATTACH_DIR2)
