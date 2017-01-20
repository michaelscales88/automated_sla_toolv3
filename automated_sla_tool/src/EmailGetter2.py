import email
import email.mime.multipart
import re
from imaplib import IMAP4_SSL, IMAP4
from collections import defaultdict
from os import listdir
from os.path import isfile, join
from datetime import timedelta, datetime


class EmailGetter(IMAP4_SSL):

    _conn_set = False

    def __init__(self, settings, parent):
        conn_info = self._get_settings(settings, parent)
        # conn_info = settings['Connection Info']['Email']
        super().__init__(conn_info['login_type'])
        self.attempt_login(conn_info['user_name'], conn_info['pw'])
        EmailGetter._conn_set = True

    def __new__(cls, settings, parent):
        return None if cls._conn_set else super().__new__(cls)
        # print('inside EmailGetter.__new__')
        # print(settings)
        # try:
        #     pass
        #     # print(parent)
        #     # print(
        #     #     '\n'.join(['{k}: {v}'.format(k=k, v=v) for k, v in kwargs.items()])
        #     # )
        #     # _settings = kwargs['Login Info']
        # except (KeyError, AttributeError):
        #     raise ValueError('No settings found for EmailGetter')
        # else:
        #     return None if cls._conn_set else super().__new__(cls)

    def __del__(self):
        try:
            print('Trying to close connection: {conn}'.format(conn=self))
            self.close()
            self.logout()
            print('Closed connection: {conn}'.format(conn=self))
        except (AttributeError, IMAP4.error):
            print('No connection to close.')
        finally:
            EmailGetter._conn_set = False

    def attempt_login(self, username, password):
        attempts = 3
        while attempts:
            try:
                r, d = self.login(username, password)
            except IMAP4.error:
                attempts -= 1
                print('There was an issue logging into: {cnx}'
                      '\n{tries} attempts remaining.'.format(cnx=username,
                                                             tries=attempts))
            else:
                conn_info = '\n'.join(
                    [
                        '{id}: {cnx}'.format(id=num, cnx=str(i, encoding='utf-8')) for num, i in enumerate(d, start=1)
                    ]
                )
                print(
                    'Connection Status: {status}'
                    '\n{conns}'.format(
                        status=r,
                        conns=conn_info
                    )
                )
                break

    def _get_settings(self, *args):
        # conf_info = {}
        for arg in args:
            print(arg)
            if hasattr(arg, 'setting'):
                print('found settings information in: {}'.format(arg))
                return arg['Connection Info']['Email']
                # conf_info[arg] = conn_info

    def get_voice_mail_info(self, all_emails):
        voice_mails = defaultdict(list)
        for subject_line in all_emails:
            client_number, phone_number, time_of_call = self.get_tokens(subject_line)
            if client_number != 0:
                voice_mails[client_number].append('{0} + {1} {2}'.format(phone_number, self.today, time_of_call))
        return voice_mails

    def all_ids(self):
        result, data = self.uid('search', None, "ALL")
        all_list = []
        if result == 'OK':
            for num in data[0].split():
                result, data = self.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])
                    all_list.append(email_message['Subject'])
        return all_list

    def read_ids(self):
        # date_sent_on = "ON " + self.today
        date_sent_on = "ON {}".format(datetime.today().date().strftime("%d-%b-%Y"))
        result, data = self.uid('search', date_sent_on, "ALL")
        read_list = []
        if result == 'OK':
            for num in data[0].split():
                result, data = self.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])
                    read_list.append(email_message['Subject'] + email_message['Date'])
        return read_list

    def get_tokens(self, search_string):
        search_object = re.search(r'(.*) > (.*?) .*', search_string, re.M | re.I)
        search_object2 = re.search(r'(.*)' + self.my_date.strftime("%Y") + ' (.*?) .*', search_string, re.M | re.I)
        if search_object:
            phone_number = search_object.group(1).replace('Voicemail', "")
            phone_number = phone_number.replace('Message', "")
            phone_number = phone_number.replace(' ', "")
            phone_number = phone_number.replace('(', "")
            client_number = search_object.group(2).replace(')', "")
            return client_number, phone_number[-4:], search_object2.group(2)
        else:
            return 0, 0, 0

    def inbox(self):
        return self.select("Inbox")

    def go_to_box(self, tgt_box):
        return self.select(tgt_box)

    def dl_f_list(self, f_list, tgt_dir, on_time=None):
        if f_list not in listdir(tgt_dir):
            on = "ON " + (self.my_date + timedelta(days=1)).strftime("%d-%b-%Y")  # change this to on_time
            status, data = self.uid('search', on, 'FROM "Chronicall Reports"')
            if status != 'OK':
                raise ValueError('Error searching Inbox.')

            # Iterating over all emails
            for msg_id in data[0].split():
                status, message_parts = self.uid('fetch', msg_id, '(RFC822)')
                if status != 'OK':
                    raise ValueError('Error fetching mail.')

                mail = email.message_from_bytes(message_parts[0][1])
                for part in mail.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    file_name = part.get_filename()

                    if bool(file_name):
                        file_path = join(tgt_dir, file_name)
                        if not isfile(file_path):
                            fp = open(file_path, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
        else:
            print("Files already downloaded.")