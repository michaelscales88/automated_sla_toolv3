from os import listdir, rename
from os.path import dirname, join, splitext, isfile
from re import sub
from datetime import timedelta, datetime, time, date
from glob import glob
from dateutil.parser import parse
from pyexcel import get_book

from automated_sla_tool.src.ReportTemplate import ReportTemplate
from automated_sla_tool.src.ReportUtilities import ReportUtilities
from automated_sla_tool.src.FinalReport import FinalReport
from automated_sla_tool.src.AppSettings import AppSettings
from automated_sla_tool.src.factory import get_email_data


class UniqueDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            super().__setitem__(key, value)


class AReport(ReportTemplate):

    def __init__(self, rpt_inr=None, test_mode=False):
        super().__init__()
        self.test_mode = test_mode
        self._util = ReportUtilities()
        self._inr = rpt_inr if rpt_inr else self.manual_input()
        self._settings = AppSettings(app=self)
        self._output = FinalReport(report_type=self._settings['report_type'],
                                   report_date=self._inr,
                                   my_report=self)
        self.req_src_files = self._settings.setting('req_src_files', rtn_val=[])

        # self.active_directory = r'{0}\{1}'.format(self.path, r'active_files')
        # self.converter_arg = r'{0}\{1}'.format(self.path, r'converter\ofc.ini')
        # self.converter_exc = r'{0}\{1}'.format(self.path, r'converter\ofc.exe')
        self.login_type = r'imap.gmail.com'
        self.user_name = r'mindwirelessreporting@gmail.com'
        self.password = r'7b!2gX4bD3'

        if isinstance(self._inr, date):
            self.util_datetime = datetime.combine(self._inr, time())
            self.day_of_wk = self._inr.weekday()
            self.src_doc_path = self.open_src_dir()
        else:
            self.util_datetime = None
            self.day_of_wk = None

    # TODO abstract this -> *args
    # TODO 2: error handling for BadZipFile error from openpyxl. handles corrupted files
    # TODO 3: Move this into ReportUtilities. Keep filter_chronicall_reports in this class
    # TODO 4: Error handling should prompt the user to redownload the file
    def load(self):
        if self._output.finished:
            return
        else:
            for (f, p) in self.loader(self.req_src_files).items():
                file = get_book(file_name=p)
                try:
                    print(f)
                    self.src_files[f] = self.filter_chronicall_reports(file)
                except (IndexError, TypeError):
                    print(self.src_files.keys())
                    print('I hit an issue opening my src file: {file}.\n'
                          'Please try to open and re-save before proceeding.'.format(file=f))
                    self.util.open_directory(self.src_doc_path)
                    raise SystemExit()
                    # self.src_files[f] = self.filter_chronicall_reports(get_book(file_name=p))
                except KeyError:
                    self.util.open_directory(self.src_doc_path)
                # self.src_files[f] = file

            if self.req_src_files:
                print('Could not find files:\n{files}'.format(
                    files='\n'.join([f for f in self.req_src_files])
                ), flush=True)
                raise SystemExit()

    # TODO if output is completed then open should open that file
    def open(self, user_string=None, sub_dir=None, alt_dir=None):
        self._output.open(str_fmt=user_string, tgt_path=alt_dir, sub_dir=sub_dir)

    def save(self, user_string=None, sub_dir=None, alt_dir=None):
        self._output.save(str_fmt=user_string, tgt_path=alt_dir, sub_dir=sub_dir)

    # OS Operations
    @property
    def util(self):
        return self._util

    def open_src_dir(self):
        file_dir = r'{dir}\{sub}\{yr}\{tgt}'.format(dir=dirname(self.path),
                                                    sub='Attachment Archive',
                                                    yr=self._inr.strftime('%Y'),
                                                    tgt=self._inr.strftime('%m%d'))
        self._util.make_dir(file_dir)
        return file_dir

    # TODO push this into ReportUtilities
    def clean_src_loc(self, spc_ch, del_ch):
        # TODO today test this more... doesn't merge/delete original file
        file_list = [f for f in listdir(self.src_doc_path) if f.endswith((".xlsx", ".xls"))]
        for f in file_list:
            f_name, ext = splitext(f)
            f_name = sub('[{spc_chrs}]'.format(spc_chrs=''.join(spc_ch)), ' ', f_name)
            f_name = sub('[{del_chs}]'.format(del_chs=''.join(del_ch)), '', f_name)
            f_name = f_name.strip()
            old_f = join(self.src_doc_path, f)
            new_f = join(self.src_doc_path, r'{f_name}{ext}'.format(f_name=f_name,
                                                                    ext=ext))
            rename(old_f, new_f)

    # TODO push this into ReportUtilities
    def loader(self, unloaded_files, need_to_dl=False):
        if need_to_dl:
            self.dl_src_files(files=unloaded_files)
            got_downloads = True
        else:
            got_downloads = False
        loaded_files = {}
        self.clean_src_loc(spc_ch=['-', '_'],
                           del_ch=['%', r'\d+'])
        for f_name in reversed(unloaded_files):
            src_f = glob(r'{f_path}*.*'.format(f_path=join(self.src_doc_path, f_name)))
            if len(src_f) is 1:
                loaded_files[f_name] = src_f[0]
                unloaded_files.remove(f_name)
        return (loaded_files
                if (len(unloaded_files) is 0 or got_downloads) else
                {**loaded_files, **self.loader(unloaded_files, need_to_dl=True)})

    # TODO push this into ReportUtilities
    def dl_src_files(self, files):
        if self._output.finished:
            return
        else:
            # TODO this should be using SlaSrcHunter.get_f_list
            self.download_chronicall_files(file_list=files)
            # src_file_directory = listdir(self.src_doc_path)
            # for file in src_file_directory:
            #     if file.endswith(".xls"):
            #         self.copy_and_convert(self.src_doc_path, src_file_directory)
            #         break

    # Report Utilities
    def manual_input(self):
        pass

    def filter_chronicall_reports(self, workbook):
        try:
            del workbook['Summary']
        except KeyError:
            pass
        for sheet_name in reversed(workbook.sheet_names()):
            sheet = workbook.sheet_by_name(sheet_name)
            del sheet.row[self.util.header_filter]
            sheet.name_rows_by_column(0)
            sheet.name_columns_by_row(0)
            try:
                self.chck_rpt_dates(sheet)
            except ValueError:
                workbook.remove_sheet(sheet_name)
        return workbook

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

    # General Utilities
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
        if file_list not in listdir(self.src_doc_path):
            try:
                imap_session = imaplib.IMAP4_SSL(self.login_type)
                status, account_details = imap_session.login(self.user_name, self.password)
                if status != 'OK':
                    raise ValueError('Not able to sign in!')

                imap_session.select("Inbox")
                on = "ON " + (self._inr + timedelta(days=1)).strftime("%d-%b-%Y")
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
                            file_path = join(self.src_doc_path, file_name)
                            if not isfile(file_path):
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
        for event in self.util.find(src_list, key):
            return_list.append(self.util.get_sec(list_to_correlate[event]))
        return return_list

    def correlate_list_val_data(self, src_list, list_to_correlate, key):
        return_list = []
        for event in self.util.find(src_list, key):
            return_list.append(list_to_correlate[event])
        return return_list

    def transmit_report(self):
        return self._output

    def check_finished(self, report_string=None, sub_dir=None, fmt='xlsx'):
        if report_string and sub_dir:
            the_file = join(self._output.save_path, sub_dir, '{file}.{ext}'.format(file=report_string, ext=fmt))
            if isfile(the_file):
                print('I know this file is completed.')
                self._output.open_existing(the_file)
            return self._output.finished
        else:
            print('No report_string in check_finished'
                  '-> Cannot check if file is completed.')

    def safe_parse_dt(self, dt_time=None, default_date=None, default_rtn=None):
        try:
            return parse(dt_time, default=(default_date if default_date is not None else self.util_datetime))
        except ValueError:
            return default_rtn if default_rtn is not None else self.util_datetime

    def parse_to_sec(self, dt=None):
        dt_t = self.util.safe_parse(dt).time()
        return self.util.convert_sec(h=dt_t.hour, m=dt_t.minute, s=dt_t.second)

    def read_time(self, time_object, spc_chr='*'):
        try:
            return_time = time_object.split(spc_chr)[0]
        except AttributeError:
            try:
                return_time = time_object.time()
            except AttributeError:
                return_time = time_object
        else:
            return_time = self.safe_parse_dt(return_time).time()
        return return_time
