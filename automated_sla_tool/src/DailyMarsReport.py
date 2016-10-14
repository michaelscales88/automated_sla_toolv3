import os
import re
import pyexcel as pe
from datetime import datetime
from collections import namedtuple
from automated_sla_tool.src.AReport import AReport
from automated_sla_tool.src.ContainerObject import ContainerObject


class DailyMarsReport(AReport):
    def __init__(self, month=None):
        super().__init__(report_dates=month)
        self.finished, report = self.report_finished()
        self.agent_time_card = (report if report is not None else self.load_documents())
        spreadsheet = r'M:\Help Desk\Schedules for OPS.xlsx'
        self.tracker = EmployeeTracker(spreadsheet, self.get_data_measurements())

    '''
    UI Section
    '''

    def query_sql_server(self):
        pass

    def prep_data(self):
        agents = self.tracker.schedule.items()
        for (ext, agent) in agents:
            sheet_name = r'{0} {1}({2})'.format(agent.f_name, agent.l_name, ext)
            todays_date_filter = pe.RowValueFilter(self.todays_date_row_filter)
            try:
                time_card = self.agent_time_card[sheet_name]
            except KeyError:
                if agent[self.day_of_wk]:
                    agent.data.set_to_key('Absent', 1)
            else:
                time_card.filter(todays_date_filter)
                self.read_timecard(time_card, agent)

    def process_report(self):
        agents = self.tracker.schedule.items()
        todays_summary = self.make_summary(['Employee', 'Time In', 'Time Out', 'Duration', 'Absent', 'Late'])
        for (ext, agent) in agents:
            data = agent.data
            # print(r'ext: {0} first: {1} last: {2}'.format(ext, agent.f_name, agent.l_name))
            # print(r'Time In: {0} Time Out: {1} Duration: {2}'.format(,
            #                                                          ,
            #                                                          ))
            # print(r'Shift Start: {0} Shift End: {1}'.format(None, None))
            # print(r'Late: {0} Absent: {1}'.format(data['Late'], data['Absent']))
            try:
                time_in = data['Logged In'].time()
            except:
                time_in = 0
            try:
                time_out = data['Logged Out'].time()
            except:
                time_out = 0
            row_name = r'{0} {1}({2})'.format(agent.f_name, agent.l_name, ext)
            new_row = [row_name,
                       time_in,
                       time_out,
                       data['Duration'],
                       data['Absent'],
                       data['Late']]
            todays_summary.row += new_row
        print(todays_summary)

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
                self.download_documents()
                agent_time_card = pe.get_book(file_name=agent_time_card_file)
            del agent_time_card['Summary']
            return self.filter_agent_time_card(agent_time_card)

    def download_documents(self):
        if self.finished:
            return
        else:
            self.download_chronicall_files()
            src_file_directory = os.listdir(self.src_doc_path)
            for file in src_file_directory:
                if file.endswith(".xls"):
                    self.copy_and_convert(self.src_doc_path, src_file_directory)
                    break

    def get_data_measurements(self):
        return self.agent_time_card[1].colnames

    def read_timecard(self, sheet, emp_data):
        start_time = emp_data[self.day_of_wk].start
        end_time = emp_data[self.day_of_wk].end
        print(start_time)
        print(end_time)
        from datetime import time, timedelta
        is_normal_shift = self.is_normal_shift(shift_time=start_time,
                                               earliest=time(3),
                                               latest=time(12))
        if is_normal_shift:
            shift_start = self.get_start_time(sheet.column['Logged In'])
            emp_data.data.set_to_key('Logged In', shift_start)
            shift_end = self.get_end_time(sheet.column['Logged Out'])
            emp_data.data.set_to_key('Logged Out', shift_end)
            if (shift_start - start_time) > timedelta(minutes=5):
                emp_data.data.set_to_key('Late', 1)
            duration = sum([self.get_sec(time_string) for time_string in sheet.column['Duration']])
            emp_data.data.set_to_key('Duration', self.convert_time_stamp(duration))
        else:
            print('After Hours')

    def get_start_time(self, column):
        try:
            return_time = min(self.safe_parse(item) for item in column).time()
        except AttributeError:
            return_time = 'No Clock In'
        return return_time

    def get_end_time(self, column):
        try:
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


class EmployeeTracker(ContainerObject):
    def __init__(self, employee_data, report_data):
        super().__init__()
        data = self.load_data(employee_data)
        self.schedule = self.create_schedule(data, report_data)

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


class EmployeeData(dict):
    def __init__(self, k_list, default):
        super().__init__()
        for key in k_list:
            self[key] = default
        self['Absent'] = default
        self['Late'] = default

    def increment_key(self, key, val):
        self[key] += val

    def set_to_key(self, key, val):
        self[key] = val

    def decrement_key(self, key, val):
        self[key] -= val

    def remove_key(self, key):
        del self[key]

