# Inherited report methods
import pyexcel as pe
import os
from datetime import timedelta, datetime
from automated_sla_tool.src.UtilityObject import UtilityObject


class AReport(UtilityObject):
    def __init__(self, report_dates=None):
        super().__init__(report_dates)
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.day_of_wk = self.dates.weekday()
        self.final_report = pe.Sheet()
        self.active_directory = r'{0}\{1}'.format(self.path, r'active_files')
        self.converter_arg = r'{0}\{1}'.format(self.path, r'converter\ofc.ini')
        self.converter_exc = r'{0}\{1}'.format(self.path, r'converter\ofc.exe')
        self.login_type = r'imap.gmail.com'
        self.user_name = r'mindwirelessreporting@gmail.com'
        self.password = r'7b!2gX4bD3'
        self.src_doc_path = self.open_src_dir()

    def set_save_path(self, report_type):
        save_path = r'{0}\Output\{1}'.format(os.path.dirname(self.path), report_type)
        self.change_dir(save_path)

    def open_src_dir(self):
        file_dir = r'{0}\{1}\{2}'.format(os.path.dirname(self.path), 'Attachment Archive', self.dates.strftime('%m%d'))
        self.change_dir(file_dir)
        return os.getcwd()

    def get_sec(self, time_string):
        try:
            h, m, s = [int(float(i)) for i in time_string.split(':')]
        except TypeError:
            return 0
        except ValueError:
            h, m = [int(float(i)) for i in time_string.split(':')]
            s = 0
        return self.convert_sec(h, m, s)

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

    def download_chronicall_files(self, file_list):
        '''
        Temporary
        self.login_type = r'imap.gmail.com'
        self.user_name = r'mindwirelessreporting@gmail.com'
        self.password = r'7b!2gX4bD3'
        '''
        import email
        import imaplib
        if file_list not in os.listdir(self.src_doc_path):
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

    def transmit_report(self):
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

    def make_summary(self, headers):
        todays_summary = pe.Sheet()
        todays_summary.row += headers
        todays_summary.name_columns_by_row(0)
        return todays_summary

    def add_time(self, dt_t, add_time=None):
        return (datetime.combine(datetime.today(), dt_t) + add_time).time()

    def report_finished(self, report_type, file_name):
        the_path = os.path.dirname(self.path)
        the_file = r'{0}\Output\{1}\{2}'.format(the_path, report_type, file_name)
        if os.path.isfile(the_file):
            file_exists = True
            the_file = pe.get_sheet(file_name=the_file)
            the_file.name_columns_by_row(0)
            the_file.name_rows_by_column(0)
        else:
            file_exists = False
            the_file = None
        return file_exists, the_file
