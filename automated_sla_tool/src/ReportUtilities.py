from datetime import datetime, date, time
from dateutil.parser import parse
from pyexcel import Book, Sheet, get_sheet, get_book
from subprocess import Popen
from re import split

from automated_sla_tool.src.UtilityObject import UtilityObject


class UniqueDict(dict):
    def __setitem__(self, key, value):
        if key not in self:
            super().__setitem__(key, value)


class BoundSettings(object):

    bound_settings = []

    @property
    def keyword(self):
        return BoundSettings.bound_settings

    @staticmethod
    def bind_settings(settings):
        BoundSettings.bound_settings = settings
        print('set bound settings')

    @staticmethod
    def clear_keyword():
        BoundSettings.bound_settings = []
        print('cleared bound settings')


class ReportUtilities(UtilityObject):

    bound_settings = BoundSettings()

    @staticmethod
    def is_weekday(raw_date):
        try:
            return ReportUtilities.day_of_week(raw_date) not in (5, 6)
        except AttributeError:
            print('{date} is invalid to get day of the week.'.format(date=raw_date))

    @staticmethod
    def day_of_week(raw_date):
        return raw_date.weekday() if isinstance(raw_date, datetime) else 'Unknown Date'

    @staticmethod
    def name_of_day(raw_date):
        return raw_date.strftime('%A') if isinstance(raw_date, datetime) else 'Unknown Date'

    @staticmethod
    def date_to_dt(raw_date):
        return datetime.combine(raw_date, time()) if isinstance(raw_date, date) else raw_date

    @staticmethod
    def phone_number(raw_number):
        rtn_val = [ch for ch in str(raw_number) if ch.isdigit()]
        return rtn_val[1:] if len(rtn_val) > 7 and rtn_val[0] == 1 else rtn_val

    @staticmethod
    def find_non_distinct(sheet=None, event_col=None):
        i_count = {}
        for row_name in reversed(sheet.rownames):
            dup_event = sheet[row_name, event_col]
            dup_info = i_count.get(dup_event, {'count': 0,
                                               'rows': []})
            dup_info['count'] += 1
            dup_info['rows'].append(row_name)
            i_count[dup_event] = dup_info
        return i_count

    @staticmethod
    def apply_format_to_wb(wb, filters=(), one_filter=None):
        for sheet in wb:
            ReportUtilities.apply_format_to_sheet(sheet, filters, one_filter)

    @staticmethod
    def apply_format_to_sheet(sheet, filters=(), one_filter=None):
        for a_filter in filters:
            del sheet.row[a_filter]
        if one_filter:
            del sheet.row[one_filter]

    @staticmethod
    def collate_wb_to_sheet(wb=()):
        headers = ['row_names'] + wb[0].colnames
        sheet_to_replace_wb = Sheet(colnames=headers)
        unique_records = UniqueDict()
        for sheet in wb:
            for i, name in enumerate(sheet.rownames):
                unique_records[name] = sheet.row_at(i)
        for rec in sorted(unique_records.keys()):
            sheet_to_replace_wb.row += [rec] + unique_records[rec]
        sheet_to_replace_wb.name_rows_by_column(0)
        return sheet_to_replace_wb

    @staticmethod
    def shortest_longest(*args):
        return (args[0], args[1]) if args[0] is min(*args, key=len) else (args[1], args[0])

    @staticmethod
    def return_selection(input_opt):
        selection = list(input_opt.values())
        return selection[
            int(
                input(
                    ''.join(['{k}: {i}\n'.format(k=k, i=i) for i, k in enumerate(input_opt)])
                )
            )
        ]

    @staticmethod
    def find(lst, a):
        return [i for i, x in enumerate(lst) if x == a]

    @staticmethod
    def is_empty_wb(book):
        if isinstance(book, Book):
            return book.number_of_sheets() is 0

    @staticmethod
    def make_summary(headers):
        todays_summary = Sheet()
        todays_summary.row += headers
        todays_summary.name_columns_by_row(0)
        return todays_summary

    # TODO consider methods like this to move into UtilityObject
    @staticmethod
    def add_time(dt_t, add_time=None):
        return (datetime.combine(datetime.today(), dt_t) + add_time).time()

    @staticmethod
    def safe_parse(dt=None):
        try:
            return parse(dt)
        except ValueError:
            print('Could not parse date_time: {dt}'.format(dt=dt))

    @staticmethod
    def open_excel(file):
        if isinstance(file, Sheet):
            return_file = file
        else:
            return_file = ReportUtilities.open_pe_file(file)
        return_file.name_columns_by_row(0)
        return_file.name_rows_by_column(0)
        return return_file

    # @staticmethod
    # def load_data(report):
    #     # load_data takes the target report and extracts the information to call loader
    #     # return_file = ReportUtilities.open_excel(file)
    #     for (f, p) in ReportUtilities.loader(report.req_src_files).items():
    #         file = get_book(file_name=p)
    #         try:
    #             print(f)
    #             report.src_files[f] = self.filter_chronicall_reports(file)
    #         except (IndexError, TypeError):
    #             print(self.src_files.keys())
    #             print('I hit an issue opening my src file: {file}.\n'
    #                   'Please try to open and re-save before proceeding.'.format(file=f))
    #             self.util.open_directory(report.src_doc_path)
    #             raise SystemExit()
    #             # self.src_files[f] = self.filter_chronicall_reports(get_book(file_name=p))
    #         except KeyError:
    #             self.util.open_directory(self.src_doc_path)
    #             # self.src_files[f] = file
    #
    #     if self.req_src_files:
    #         print('Could not find files:\n{files}'.format(
    #             files='\n'.join([f for f in self.req_src_files])
    #         ), flush=True)
    #         raise SystemExit()
    #     return return_file
    #
    # # TODO push this into ReportUtilities
    # @staticmethod
    # def loader(unloaded_files, need_to_dl=False):
    #     if need_to_dl:
    #         self.dl_src_files(files=unloaded_files)
    #         got_downloads = True
    #     else:
    #         got_downloads = False
    #     loaded_files = {}
    #     self.clean_src_loc(spc_ch=['-', '_'],
    #                        del_ch=['%', r'\d+'])
    #     for f_name in reversed(unloaded_files):
    #         src_f = glob(r'{f_path}*.*'.format(f_path=join(self.src_doc_path, f_name)))
    #         if len(src_f) is 1:
    #             loaded_files[f_name] = src_f[0]
    #             unloaded_files.remove(f_name)
    #     return (loaded_files
    #             if (len(unloaded_files) is 0 or got_downloads) else
    #             {**loaded_files, **self.loader(unloaded_files, need_to_dl=True)})

    # TODO build out ReportUtility to open pe files for sheets/books
    @staticmethod
    def open_pe_file(f_name):
        try:
            return get_book(file_name=f_name)
        except OSError:
            print('OSError ->'
                  'cannot open {}'.format(f_name))

    @staticmethod
    def safe_div(num, denom):
        rtn_val = 0
        try:
            rtn_val = num / denom
        except ZeroDivisionError:
            pass
        return rtn_val

    # Generator Section
    @staticmethod
    def common_keys(*dcts):
        for i in set(dcts[0]).intersection(*dcts[1:]):
            yield (i,) + tuple(d[i] for d in dcts)

    @staticmethod
    def return_matches(*args, match_val=None):
        if len(args) == 2:
            shortest_list, longest_list = ReportUtilities.shortest_longest(*args)
            longest_list_indexed = {}
            for item in longest_list:
                longest_list_indexed[item[match_val]] = item
            for item in shortest_list:
                if item[match_val] in longest_list_indexed:
                    yield item, longest_list_indexed[item[match_val]]

    # Filter Section
    @staticmethod
    def header_filter(row_index, row):
        corner_case = split('\(| - ', row[0])
        # bad_word = corner_case[0].split(' ')[0] not in ('Feature', 'Call', 'Event')
        bad_word = corner_case[0].split(' ')[0] not in ReportUtilities.bound_settings.keyword
        return True if len(corner_case) > 1 else bad_word

    @staticmethod
    def blank_row_filter(row_index, row):
        result = [element for element in str(row[3]) if element != '']
        return len(result) == 0

    @staticmethod
    def answered_filter(row_index, row):
        try:
            answered = row[-5]
        except ValueError:
            answered = False
        return answered

    @staticmethod
    def inbound_call_filter(row_index, row):
        return row[0] not in ('Inbound', 'Call Direction')

    @staticmethod
    def zero_duration_filter(row_index, row):
        result = [element for element in row[-1] if element != '']
        return len(result) == 0

    @staticmethod
    def remove_internal_inbound_filter(row_index, row):
        return row[-2] == row[-3]

    @staticmethod
    def open_directory(tgt_dir):
        Popen('explorer "{0}"'.format(tgt_dir))
        input('Any key to continue.')
