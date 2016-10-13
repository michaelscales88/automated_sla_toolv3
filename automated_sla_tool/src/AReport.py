# Inherited report methods
import pyexcel as pe
import os
from datetime import timedelta, time, datetime
from dateutil.parser import parse


class AReport:
    def __init__(self, report_dates=None):
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if report_dates is None:
            raise ValueError('No report date provided... Try again.')
        self.dates = report_dates
        self.util_datetime = datetime.combine(self.dates, time())
        self.day_of_wk = self.dates.weekday()
        self.final_report = pe.Sheet()
        self.active_directory = r'{0}\{1}'.format(self.path, r'active_files')
        self.converter_arg = r'{0}\{1}'.format(self.path, r'converter\ofc.ini')
        self.converter_exc = r'{0}\{1}'.format(self.path, r'converter\ofc.exe')
        self.login_type = r'imap.gmail.com'
        self.user_name = r'mindwirelessreporting@gmail.com'
        self.password = r'7b!2gX4bD3'
        self.src_doc_path = None

    def get_sec(self, time_string):
        try:
            h, m, s = [int(float(i)) for i in time_string.split(':')]
        except TypeError:
            return 0
        return self.convert_sec(h, m, s)

    def change_dir(self, the_dir):
        try:
            os.chdir(the_dir)
        except FileNotFoundError:
            try:
                os.makedirs(the_dir, exist_ok=True)
                os.chdir(the_dir)
            except OSError:
                pass

    def convert_sec(self, h, m, s):
        return (3600 * int(h)) + (60 * int(m)) + int(s)

    def copy_and_convert(self, file_location, directory):
        from shutil import move
        for src_file in directory:
            if src_file.endswith(".xls"):
                src = os.path.join(file_location, src_file)
                des = os.path.join(self.active_directory, src_file)
                move(src, des)

        import subprocess as proc
        proc.run([self.converter_exc, self.converter_arg])
        filelist = [f for f in os.listdir(self.active_directory) if f.endswith(".xls")]
        for f in filelist:
            f = os.path.join(self.active_directory, f)
            os.remove(f)

        for src_file in os.listdir(self.active_directory):
            src = os.path.join(self.active_directory, src_file)
            des = os.path.join(file_location, src_file)
            move(src, des)

    def convert_time_stamp(self, convert_seconds):
        minutes, seconds = divmod(convert_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{0}:{1:02d}:{2:02d}".format(hours, minutes, seconds)

    def prepare_sheet_header(self, lst, first_index):
        return_list = [i for i in lst]
        return_list.insert(0, first_index)
        return [return_list]

    def download_chronicall_files(self):
        '''
        Temporary
        self.login_type = r'imap.gmail.com'
        self.user_name = r'mindwirelessreporting@gmail.com'
        self.password = r'7b!2gX4bD3'
        '''
        import email
        import imaplib
        file_dir = r'{0}\{1}\{2}'.format(os.path.dirname(self.path), 'Attachment Archive', self.dates.strftime('%m%d'))
        self.change_dir(file_dir)
        self.src_doc_path = os.getcwd()
        if not os.listdir(self.src_doc_path):
            try:
                imap_session = imaplib.IMAP4_SSL(self.login_type)
                status, account_details = imap_session.login(self.user_name, self.password)
                if status != 'OK':
                    raise ValueError('Not able to sign in!')

                imap_session.select("Inbox")
                on = "ON " + (self.dates + timedelta(days=1)).strftime("%d-%b-%Y")
                status, data = imap_session.uid('search', on, 'FROM "Chronicall Reports"')
                if status != 'OK':
                    raise ValueError('Error searching Inbox.')

                # Iterating over all emails
                for msg_id in data[0].split():
                    status, message_parts = imap_session.uid('fetch', msg_id, '(RFC822)')
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
                            file_path = os.path.join(file_name)
                            if not os.path.isfile(file_path):
                                fp = open(file_path, 'wb')
                                fp.write(part.get_payload(decode=True))
                                fp.close()

                imap_session.close()
                imap_session.logout()

            except Exception as err:
                raise ValueError('Not able to download all attachments. Error: {}'.format(err))
        else:
            print("Files already downloaded.")

    def str_to_bool(self, bool_str):
        if type(bool_str) is bool:
            return bool_str
        elif bool_str in ('True', 'TRUE', 'true'):
            return True
        elif bool_str in ('False', 'false', 'FALSE'):
            return False
        else:
            raise ValueError("Cannot covert {} to a bool".format(bool_str))

    def transmit_report(self):
        self.final_report.name_rows_by_column(0)
        return self.final_report

    def make_distinct_and_sort(self, worksheet):
        worksheet.name_rows_by_column(0)
        sorted_list = [item for item in sorted(worksheet.rownames, reverse=False) if '-' not in item]
        new_sheet = pe.Sheet()
        for item in sorted_list:
            temp_list = worksheet.row[item]
            temp_list.insert(0, item)
            new_sheet.row += temp_list
        return new_sheet

    def safe_parse(self, date=None, default=None, default_rtn=None):
        try:
            return parse(date, default=(default if default is not None else self.util_datetime))
        except ValueError:
            return default_rtn

    def make_summary(self, headers):
        todays_summary = pe.Sheet()
        todays_summary.row += headers
        todays_summary.name_columns_by_row(0)
        return todays_summary
