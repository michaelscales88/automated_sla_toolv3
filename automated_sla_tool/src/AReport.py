import pyexcel as pe
import os
import re
from os.path import dirname, join, abspath
from datetime import timedelta, datetime, time, date
from glob import glob
from dateutil.parser import parse
from automated_sla_tool.src.UtilityObject import UtilityObject
from automated_sla_tool.src.FinalReport import FinalReport


class UniqueDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            dict.__setitem__(self, key, value)


class AReport(UtilityObject):
    def __init__(self,
                 report_dates=None,
                 report_type=None):
        super().__init__()
        if report_dates is None:
            raise ValueError('No report date provided... Try again.')
        self.dates = report_dates
        self.fr = FinalReport(report_type=report_type, report_date=self.dates, my_report=self)
        self.src_files = {}
        self.req_src_files = []
        self.path = dirname(dirname(abspath(__file__)))
        self.active_directory = r'{0}\{1}'.format(self.path, r'active_files')
        self.converter_arg = r'{0}\{1}'.format(self.path, r'converter\ofc.ini')
        self.converter_exc = r'{0}\{1}'.format(self.path, r'converter\ofc.exe')
        self.login_type = r'imap.gmail.com'
        self.user_name = r'mindwirelessreporting@gmail.com'
        self.password = r'7b!2gX4bD3'
        if isinstance(self.dates, date):
            self.util_datetime = datetime.combine(self.dates, time())
            self.day_of_wk = self.dates.weekday()
            self.src_doc_path = self.open_src_dir()
        else:
            self.util_datetime = None
            self.day_of_wk = None

    def load_documents(self):
        # TODO abstract this -> *args
        if self.fr.finished:
            return
        else:
            for (f, p) in self.loader(self.req_src_files).items():
                file = pe.get_book(file_name=p)
                self.src_files[f] = self.filter_chronicall_reports(file)
            if self.req_src_files:
                print(self.src_files)
                print(self.req_src_files)
                print('Could not find files:\n{files}'.format(
                    files='\n'.join([f for f in self.req_src_files])
                ), flush=True)
                raise SystemExit()

    def save(self, user_string=None, sub_dir=None, alt_dir=None):
        self.fr.save(str_fmt=user_string, tgt_path=alt_dir, sub_dir=sub_dir)

    '''
    OS Operations
    '''

    def open_src_dir(self):
        file_dir = r'{dir}\{sub}\{yr}\{tgt}'.format(dir=os.path.dirname(self.path),
                                                    sub='Attachment Archive',
                                                    yr=self.dates.strftime('%Y'),
                                                    tgt=self.dates.strftime('%m%d'))
        self.change_dir(file_dir)
        return os.getcwd()

    def clean_src_loc(self, spc_ch, del_ch):
        # TODO today test this more... doesn't merge/delete original file
        file_list = [f for f in os.listdir(self.src_doc_path) if f.endswith((".xlsx", ".xls"))]
        for f in file_list:
            f_name, ext = os.path.splitext(f)
            f_name = re.sub('[{spc_chrs}]'.format(spc_chrs=''.join(spc_ch)), ' ', f_name)
            f_name = re.sub('[{del_chs}]'.format(del_chs=''.join(del_ch)), '', f_name)
            f_name = f_name.strip()
            os.rename(f, r'{0}{1}'.format(f_name, ext))

    # this doesn't need to go deep twice if files found on first pass
    def loader(self, unloaded_files, run2=False):
        if run2 is True:
            return {}
        loaded_files = {}
        self.clean_src_loc(spc_ch=['-', '_'],
                           del_ch=['%', r'\d+'])
        for f_name in reversed(unloaded_files):
            src_f = glob(r'{0}\{1}*.xlsx'.format(self.src_doc_path, f_name))
            if len(src_f) is 1:
                loaded_files[f_name] = src_f[0]
                unloaded_files.remove(f_name)
            else:
                # TODO additional error handling for file names that have not been excluded?
                pass
        if unloaded_files:
            self.download_documents(files=unloaded_files)
            return {**loaded_files, **self.loader(unloaded_files, True)}
        else:
            return loaded_files

    def download_documents(self, files):
        if self.fr.finished:
            return
        else:
            self.download_chronicall_files(file_list=files)
            src_file_directory = os.listdir(self.src_doc_path)
            for file in src_file_directory:
                if file.endswith(".xls"):
                    self.copy_and_convert(self.src_doc_path, src_file_directory)
                    break

    '''
    Report Utilities
    '''

    def apply_formatters_to_wb(self, wb, filters=(), one_filter=None):
        for sheet in wb:
            self.apply_formatters_to_sheet(sheet, filters, one_filter)

    def apply_formatters_to_sheet(self, sheet, filters=(), one_filter=None):
        for a_filter in filters:
            this_filter = pe.RowValueFilter(a_filter)
            sheet.filter(this_filter)
        if one_filter:
            this_filter = pe.RowValueFilter(one_filter)
            sheet.filter(this_filter)

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

    def filter_chronicall_reports(self, workbook):
        try:
            del workbook['Summary']
        except KeyError:
            pass
        chronicall_report_filter = pe.RowValueFilter(self.header_filter)
        for sheet_name in reversed(workbook.sheet_names()):
            sheet = workbook[sheet_name]
            sheet.filter(chronicall_report_filter)
            sheet.name_columns_by_row(0)
            sheet.name_rows_by_column(0)
            try:
                self.chck_rpt_dates(sheet)
            except ValueError:
                print('removing {sheet_name}'.format(sheet_name=sheet_name))
                workbook.remove_sheet(sheet_name)
        return workbook

    def header_filter(self, row):
        corner_case = re.split('\(| - ', row[0])
        bad_word = corner_case[0].split(' ')[0] not in ('Feature', 'Call', 'Event')
        return True if len(corner_case) > 1 else bad_word

    def chck_rpt_dates(self, sheet):
        first = self.chck_w_in_days(sheet.column['Start Time'][0])
        try:
            last = self.chck_w_in_days(sheet.column['End Time'][-1])
        except ValueError:
            last = False
        if first or last:
            pass
        else:
            raise ValueError

    def collate_wb_to_sheet(self, wb=()):
        headers = ['row_names'] + wb[0].colnames
        sheet_to_replace_wb = pe.Sheet(colnames=headers)
        unique_records = UniqueDict()
        for sheet in wb:
            for i, name in enumerate(sheet.rownames):
                unique_records[name] = sheet.row_at(i)
        for rec in sorted(unique_records.keys()):
            sheet_to_replace_wb.row += [rec] + unique_records[rec]
        sheet_to_replace_wb.name_rows_by_column(0)
        return sheet_to_replace_wb

    '''
    General Utilities
    '''

    # TODO make a typedef decorator

    def return_selection(self, input_opt):
        selection = list(input_opt.values())
        return selection[
            int(
                input(
                    ''.join(['{k}: {i}\n'.format(k=k, i=i) for i, k in enumerate(input_opt)])
                )
            )
        ]

    def chck_w_in_days(self, doc_dt, num_days=1):
        try:
            date_time = parse(doc_dt)
        except ValueError:
            return False
        else:
            if (date_time - self.util_datetime) <= timedelta(days=num_days):
                return True
            else:
                return False

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

    # TODO these can be removed once MarsReport is refactored to crawl reports SlaReport E.g. for row and col in rpt
    def correlate_list_time_data(self, src_list, list_to_correlate, key):
        return_list = []
        for event in self.find(src_list, key):
            return_list.append(self.get_sec(list_to_correlate[event]))
        return return_list

    def correlate_list_val_data(self, src_list, list_to_correlate, key):
        return_list = []
        for event in self.find(src_list, key):
            return_list.append(list_to_correlate[event])
        return return_list

    def find(self, lst, a):
        return [i for i, x in enumerate(lst) if x == a]

    def is_empty_wb(self, book):
        if type(book) is not pe.Book:
            return
        return book.number_of_sheets() is 0

    def transmit_report(self):
        return self.fr

    def make_summary(self, headers):
        todays_summary = pe.Sheet()
        todays_summary.row += headers
        todays_summary.name_columns_by_row(0)
        return todays_summary

    def add_time(self, dt_t, add_time=None):
        return (datetime.combine(datetime.today(), dt_t) + add_time).time()

    def check_finished(self, report_string=None, sub_dir=None, fmt='xlsx'):
        if report_string and sub_dir:
            the_file = join(self.fr.save_path, sub_dir, '{file}.{ext}'.format(file=report_string, ext=fmt))
            if os.path.isfile(the_file):
                self.fr.open_report(the_file)
            return self.fr.finished
        else:
            print('No report_string in check_finished'
                  '-> Cannot check if file is completed.')

    def safe_parse(self, dt_time=None, default_date=None, default_rtn=None):
        try:
            return parse(dt_time, default=(default_date if default_date is not None else self.util_datetime))
        except ValueError:
            return default_rtn if default_rtn is not None else self.util_datetime

    def read_time(self, time_object, spc_chr='*'):
        try:
            return_time = time_object.split(spc_chr)[0]
        except AttributeError:
            try:
                return_time = time_object.time()
            except AttributeError:
                return_time = time_object
        else:
            return_time = self.safe_parse(return_time).time()
        return return_time
