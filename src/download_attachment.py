# Something in lines of http://stackoverflow.com/questions/348630/how-can-i-download
# -all-emails-with-attachments-from-gmail
# Make sure you have IMAP enabled in your gmail settings.
# Right now it won't download same file name twice even if their contents are different.

import datetime
import email
import imaplib
import os

from src.CONSTANTS import SELF_PATH


def download_attachments(use_date, login_type, user_name, password, attachment_directory):

    os.chdir(os.path.dirname(SELF_PATH) + attachment_directory)
    if attachment_directory == "\\\\Attachment Archive\\\\":
        folder_date = (use_date - datetime.timedelta(days=1)).strftime("%m%d")
        try:
            print(folder_date)
            os.mkdir(folder_date)
        except OSError:
            print("Folder %s already exists." % folder_date)
            pass
        finally:
            os.chdir(os.path.dirname(SELF_PATH) + attachment_directory + folder_date + '\\')
    cwd = os.getcwd()
    if not os.listdir(cwd):
        try:
            imap_session = imaplib.IMAP4_SSL(login_type)
            status, account_details = imap_session.login(user_name, password)
            if status != 'OK':
                print('Not able to sign in!')
                raise ValueError

            imap_session.select("Inbox")
            on = "ON " + use_date.strftime("%d-%b-%Y")
            status, data = imap_session.uid('search', on, 'FROM "Chronicall Reports"')
            if status != 'OK':
                print('Error searching Inbox.')
                raise ValueError

            # Iterating over all emails
            for msg_id in data[0].split():
                status, message_parts = imap_session.uid('fetch', msg_id, '(RFC822)')
                if status != 'OK':
                    print('Error fetching mail.')
                    raise ValueError

                mail = email.message_from_bytes(message_parts[0][1])
                for part in mail.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    file_name = part.get_filename()

                    if bool(file_name):
                        file_path = os.path.join(file_name)
                        if not os.path.isfile(file_path):
                            fp = open(file_path, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()

            imap_session.close()
            imap_session.logout()

        except Exception as e:
            print('Not able to download all attachments.')
            print(e)
    else:
        print("Files already downloaded.")
