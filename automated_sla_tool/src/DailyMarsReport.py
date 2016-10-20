import os
import re
import pyexcel as pe
from datetime import datetime, time, timedelta
from collections import namedtuple
from automated_sla_tool.src.AReport import AReport
from automated_sla_tool.src.ContainerObject import ContainerObject
from automated_sla_tool.src.Notes import Notes


class DailyMarsReport(AReport):
    def __init__(self, month=None):
        super().__init__(report_dates=month)
        self.finished, report = self.report_finished()
        self.agent_time_card = (report if report is not None else self.load_documents())
        spreadsheet = r'M:\Help Desk\Schedules for OPS.xlsx'
        self.tracker = EmployeeTracker(spreadsheet, self.get_data_measurements())
        self.notes = Notes()

    '''
    UI Section
    '''

    def query_sql_server(self):
        pass

    def prep_data(self):
        agents = self.tracker.get_tracker()
        for (ext, agent) in agents.items():
            sheet_name = r'{0} {1}({2})'.format(agent.f_name, agent.l_name, ext)
            todays_date_filter = pe.RowValueFilter(self.todays_date_row_filter)
            try:
                time_card = self.agent_time_card[sheet_name]
            except KeyError:
                if agent[self.day_of_wk]:
                    agent.data['Absent'] = 1
            else:
                time_card.filter(todays_date_filter)
                self.read_timecard(time_card, agent)

    def process_report(self):
        agents = self.tracker.get_tracker()
        todays_summary = self.make_summary(self.tracker.get_header())
        for (ext, agent) in agents.items():
            todays_summary.row += self.tracker[ext]

        notes = [self.notes.pop(0)]
        todays_summary.row += notes
        todays_summary.row += self.notes.get_notes()

        todays_summary.name_rows_by_column(0)
        print(todays_summary)

        todays_summary.save_as(r'C:\Users\mscales\Desktop\Development', )

    def save_report(self):
        pass

    '''
    Utilities Section
    '''

    def load_documents(self):
        if self.finished:
            return
        else:
            agent_time_card_file = r'{0}\{1}'.format(self.src_doc_path, r'Agent Time Card.xlsx')
            try:
                agent_time_card = pe.get_book(file_name=agent_time_card_file)
            except FileNotFoundError:
                self.download_documents(files=['Agent Time Card.xlsx'])
                agent_time_card = pe.get_book(file_name=agent_time_card_file)
            del agent_time_card['Summary']
            return self.filter_agent_time_card(agent_time_card)

    def download_documents(self, files):
        if self.finished:
            return
        else:
            self.download_chronicall_files(file_list=files)
            src_file_directory = os.listdir(self.src_doc_path)
            for file in src_file_directory:
                if file.endswith(".xls"):
                    self.copy_and_convert(self.src_doc_path, src_file_directory)
                    break

    def get_data_measurements(self):
        return self.agent_time_card[1].colnames

    def read_timecard(self, sheet, emp_data):
        start_time = emp_data[self.day_of_wk].start
        is_normal_shift = self.is_normal_shift(shift_time=start_time,
                                               earliest=time(hour=0),
                                               latest=time(hour=18, minute=59))
        if is_normal_shift:
            emp_data.data['Logged In'] = self.get_start_time(sheet.column['Logged In'])
            emp_data.data['Logged Out'] = self.get_end_time(sheet.column['Logged Out'])
            if emp_data.data['Logged In'] >= self.check_grace_pd(start_time, minutes=timedelta(minutes=5)):
                emp_data.data['Late'] = 1
            duration = sum([self.get_sec(time_string) for time_string in sheet.column['Duration']])
            emp_data.data['Duration'] = self.convert_time_stamp(duration)
        else:
            start_full_dt = self.get_start_time(sheet.column['Logged In'], overnight=True)
            end_full_dt = self.get_end_time(sheet.column['Logged Out'], overnight=True)
            emp_data.data['Logged In'] = self.notes.add_time_note(start_full_dt)
            emp_data.data['Logged Out'] = self.notes.add_time_note(end_full_dt)

    def get_start_time(self, column, overnight=False):
        try:
            if overnight:
                return_time = max(self.safe_parse(item) for item in column)
            else:
                return_time = min(self.safe_parse(item) for item in column).time()
        except AttributeError:
            return_time = 'No Clock In'
        return return_time

    def get_end_time(self, column, overnight=False):
        try:
            if overnight:
                return_time = max(self.safe_parse(item) for item in column)
            else:
                return_time = max(self.safe_parse(item) for item in column).time()
        except AttributeError:
            return_time = 'No Clock Out'
        return return_time

    def get_page_as_num(self, sheet_name):
        return_value = re.findall(r'\b\d+\b', sheet_name)
        if len(return_value) != 1:
            raise NameError('In MarsReport.get_page_as_num'
                            'Error reading page number'
                            '-> bad sheet name')
        return return_value[0]

    def report_finished(self):
        return False, None

    def filter_agent_time_card(self, workbook):
        time_card_filter = pe.RowValueFilter(self.agent_time_row_filter)
        for sheet in workbook:
            sheet.filter(time_card_filter)
            sheet.name_columns_by_row(0)
            sheet.name_rows_by_column(0)
        return workbook

    def agent_time_row_filter(self, row):
        unique_cell = row[0].split(' ')
        return unique_cell[0] != 'Feature'

    def todays_date_row_filter(self, row):
        # TODO: Simplify... this seems overly complicated...
        dates = [self.safe_parse(date=cell, default_rtn=self.util_datetime).date() for cell in row]
        return False in [(self.dates == date) for date in dates]

    def is_normal_shift(self, shift_time=None, earliest=None, latest=None):
        return earliest <= shift_time <= latest

    def check_grace_pd(self, dt_t, minutes):
        return self.add_time(dt_t, add_time=minutes)


class EmployeeTracker(ContainerObject):
    def __init__(self, employee_data, report_data):
        super().__init__()
        data = self.load_data(employee_data)
        self.__data = self.create_schedule(data, report_data)

    def load_data(self, file):
        return_file = super().load_data(file)
        return_file.name_columns_by_row(0)
        return_file.name_rows_by_column(0)
        return return_file

    def create_schedule(self, data, report_data):
        return_dict = {}
        new_schedule = namedtuple('this_emp', 'Monday Tuesday Wednesday Thursday Friday '
                                              'Saturday Sunday f_name l_name data')
        new_schedule.__new__.__defaults__ = (None,) * len(new_schedule._fields)
        for emp in data.rownames:
            emp_schedule = new_schedule(f_name=data[emp, 'First'],
                                        l_name=data[emp, 'Last'],
                                        Monday=self.date_factory(data[emp, 'Monday']),
                                        Tuesday=self.date_factory(data[emp, 'Tuesday']),
                                        Wednesday=self.date_factory(data[emp, 'Wednesday']),
                                        Thursday=self.date_factory(data[emp, 'Thursday']),
                                        Friday=self.date_factory(data[emp, 'Friday']),
                                        Saturday=self.date_factory(data[emp, 'Saturday']),
                                        Sunday=self.date_factory(data[emp, 'Sunday']),
                                        data=EmployeeData(report_data, 0))
            return_dict[emp] = emp_schedule
        return return_dict

    def date_factory(self, date_string):
        dt = namedtuple('date', 'start end')
        try:
            (raw_start, raw_end) = self.split_str(date_string)
        except ValueError:
            return_dt = None
        else:
            dt_start = datetime.strptime(raw_start, '%H:%M').time()
            dt_end = datetime.strptime(raw_end, '%H:%M').time()
            return_dt = dt(start=dt_start, end=dt_end)
        return return_dt

    def split_str(self, t_string):
        return t_string.split('-')

    def __getitem__(self, ext):
        agent_data = self.__data[ext]
        row_name = r'{0} {1}({2})'.format(agent_data.f_name, agent_data.l_name, ext)
        return [row_name] + agent_data.data.get_row()

    def get_tracker(self):
        return self.__data

    def get_header(self):
        return ['Employee'] + sorted(next(iter(self.__data.values())).data.keys())


class EmployeeData(object):
    def __init__(self, k_list, default):
        self.__dict = {}
        for key in k_list:
            self.__dict[key] = default
        self.__dict['Absent'] = default
        self.__dict['Late'] = default

    def increment_key(self, key, val):
        if key not in self.__dict:
            raise KeyError("The key {} is not defined.".format(key))
        self.__dict[key] += val

    def __setitem__(self, key, item):
        if key not in self.__dict:
            raise KeyError("The key {} is not defined.".format(key))
        self.__dict[key] = item

    def __getitem__(self, key):
        return self.__dict[key]

    def get_row(self):
        return [self.__dict[k] for k in sorted(self.__dict.keys())]

    def keys(self):
        return self.__dict.keys()
