import email
import email.mime.multipart
import io
from  tempfile import NamedTemporaryFile
import base64
from imaplib import IMAP4_SSL, IMAP4
from pyexcel import Book, get_book, get_sheet, Sheet, to_dict, load_from_memory
from collections import defaultdict
from os import listdir, getcwd
from os.path import isfile, join
from datetime import timedelta, datetime
from traceback import format_exc

from automated_sla_tool.src.AppSettings import AppSettings


class EmailGetter(IMAP4_SSL):
    def __init__(self, settings, parent):
        conn_info = self._get_conn_settings(settings, parent)
        self._settings = AppSettings(self)
        try:
            print(
                'Attempting to connect to {conn_type} : {connection}'.format(
                    conn_type=conn_info['login_type'],
                    connection=conn_info['user_name']
                )
            )
            super().__init__(conn_info['login_type'])
            self.attempt_login(conn_info['user_name'], conn_info['pw'])
        except AttributeError:
            print(
                'No settings found for EmailGetter.'
            )
        except KeyError:
            print(
                'No connection information provided for EmailGetter.'
            )
        except IMAP4.error as e:
            print(
                'Encountered {e} during connection to:\n'
                '{conn_type} : {connection}\n'
                '{error_log}'.format(
                    e=e,
                    conn_type=conn_info('login_type', 'No connection type provided.'),
                    connection=conn_info('user_name', 'No email to connect to.'),
                    error_log=format_exc()
                )
            )

    def __new__(cls, settings, parent):
        try:
            return parent.instances[cls] if cls in parent.instances else super().__new__(cls)
        except AttributeError:
            return super().__new__(cls)

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

    '''
    Connection Operations
    '''

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

    @staticmethod
    def _get_conn_settings(*args):
        conn_info = None
        for arg in args:
            if hasattr(arg, 'setting'):
                try:
                    conn_info = arg['Connection Info']['Email']
                except KeyError:
                    print('No settings found:\n'
                          '[Connection Info]\n'
                          '[[Email]]\n'
                          'for property: {arg}'.format(arg=arg))
                else:
                    break
        return conn_info

    '''
    Email Operations
    '''

    @staticmethod
    def get_payload(email_info):
        payload = {}
        for part in email_info.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            f_name = part.get_filename()
            # f_ext = '.{type}'.format(type=part.get_content_type())
            f_ext = '{type}'.format(type='xlsx')
            # print(f_ext)
            print(part.get_content_type())

            # if bool(f_name):
            #     # values = io.BytesIO(part.get_payload(decode=True)).getvalue()
            #     with NamedTemporaryFile(mode='w+b', suffix=f_ext) as f:
            #         f.write(part.get_payload(decode=True))
            #         f.seek(0)
            #         payload[f_name] = get_book(file_type=f_ext,
            #                                    file_content=f.read()
            #                                    )
        # else:
        #     print(email_info.get_payload(decode=True))
        return payload

    def go_to_box(self, tgt_box):
        return self.select(tgt_box)

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
        read_ids = {}
        date_sent_on = "ON {}".format(datetime.today().date().strftime("%d-%b-%Y"))
        for email_info in self._search(date_sent_on):
            read_id = {
                'from': email_info.get('From', None),
                'dt': email_info.get('Date', None),
                'subject': email_info.get('Subject', None),
                'payload': self.get_payload(email_info)
            }
            read_ids[read_id['subject']] = read_id
            # break
            # print(email_info)
            # break
        for k, v in read_ids.items():
            print(k)
            print(v['payload'])

        result, data = self.uid('search', date_sent_on, 'all')

        read_list = []
        if result == 'OK':
            for num in data[0].split():
                result, data = self.uid('fetch', num, '(RFC822)')
                if result == 'OK':
                    email_message = email.message_from_bytes(data[0][1])
                    read_list.append(email_message['Subject'] + email_message['Date'])
        return read_list

    '''
    Iterator
    '''

    def _search(self, look_for):
        result, data = self.uid('search', look_for, 'all')
        if result == 'OK':
            for uid in data[0].split():
                result, data = self.uid('fetch', uid, '(RFC822)')
                if result == 'OK':
                    yield (email.message_from_bytes(data[0][1]))
