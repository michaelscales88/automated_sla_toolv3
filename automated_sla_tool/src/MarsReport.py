import os
import re
import pyexcel as pe
from collections import namedtuple
from dateutil.parser import parse
from automated_sla_tool.src.AReport import AReport
from automated_sla_tool.src.ContainerObject import ContainerObject


class MarsReport(AReport):
    def __init__(self, month=None):
        super().__init__(report_dates=month)
        self.finished, report = self.report_finished()
        self.agent_time_card = None
        spreadsheet = r'M:\Help Desk\Schedules for OPS.xlsx'
        self.tracker = EmployeeTracker(spreadsheet)

    '''
    UI Section
    '''

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

    def daily_report(self):
        pass

    def query_sql_server(self):
        pass

    def load_documents(self):
        if self.finished:
            return
        else:
            agent_time_card_file = r'{0}\{1}'.format(self.src_doc_path, r'Agent Time Card.xlsx')

            agent_time_card = pe.get_book(file_name=agent_time_card_file)
            del agent_time_card['Summary']
            self.agent_time_card = self.filter_agent_time_card(agent_time_card)

    def compile_data(self):
        todays_summary = pe.Sheet()
        todays_summary.row += ['Employee', 'Time In', 'Time Out', 'Duration']
        todays_summary.name_columns_by_row(0)
        for sheet in self.agent_time_card:
            min_time = min([parse(date) for date in sheet.column['Logged In']])
            max_time = max([parse(date) for date in sheet.column['Logged Out']])
            duration = sum([self.get_sec(time) for time in sheet.column['Duration']])
            new_row = [sheet.name, min_time.time(), max_time.time(), self.convert_time_stamp(duration)]
            todays_summary.row += new_row
        print(self.agent_time_card)
        print(todays_summary)
        new_book = pe.Book()
        new_book += todays_summary
        new_book += self.agent_time_card
        print(new_book)
        # self.agent_time_card

    def process_report(self):
        date = self.dates.weekday()
        for sheet in self.agent_time_card:
            try:
                emp_num = self.get_page_as_num(sheet.name)
                emp_info = self.tracker.schedule[emp_num]
                emp_schedule = emp_info[date]
                (start_time, end_time) = self.read_today_schedule(emp_schedule)
            except KeyError:
                pass
            else:
                min_time = min([parse(date) for date in sheet.column['Logged In']])
                max_time = max([parse(date) for date in sheet.column['Logged Out']])
                duration = sum([self.get_sec(time) for time in sheet.column['Duration']])
                print(r'time stuff for: {0} {1}'.format(emp_info.f_name, emp_info.l_name))
                print(start_time)
                print(min_time)
                print(end_time)
                print(max_time)
                print(self.convert_time_stamp(duration))

    def save_report(self):
        pass

    '''
    Utilities Section
    '''
    def read_today_schedule(self, emp_schedule):
        return emp_schedule.split('-')

    def get_page_as_num(self, sheet_name):
        return_value = re.findall(r'\b\d+\b', sheet_name)
        if len(return_value) != 1:
            raise NameError('In MarsReport.get_page_as_num'
                            'Error reading page number'
                            '-> bad sheet name')
        return return_value[0]

    def print_sheet_v(self):
        for sheet in self.agent_time_card:
            print(sheet)
            min_time = min([parse(date) for date in sheet.column['Logged In']])
            max_time = max([parse(date) for date in sheet.column['Logged Out']])
            # duration = sum([self.get_sec(time) for time in sheet.column['Duration']])
            print(min_time)
            print(max_time)

    def report_finished(self):
        return False, None

    def filter_agent_time_card(self, workbook):
        time_card_filter = pe.RowValueFilter(self.agent_time_row_filter)
        for sheet in workbook:
            sheet.filter(time_card_filter)
            sheet.name_columns_by_row(0)
        return workbook

    def agent_time_row_filter(self, row):
        unique_cell = row[0].split(' ')
        return unique_cell[0] != 'Feature'


class EmployeeTracker(ContainerObject):
    def __init__(self, employee_data):
        super().__init__()
        data = self.load_data(employee_data)
        self.schedule = self.read_schedule(data)

    def load_data(self, file):
        return_file = super().load_data(file)
        return_file.name_columns_by_row(0)
        return_file.name_rows_by_column(0)
        return return_file

    def read_schedule(self, data):
        return_dict = {}
        new_schedule = namedtuple('this_emp', 'Monday Tuesday Wednesday Thursday Friday Saturday Sunday f_name l_name')
        new_schedule.__new__.__defaults__ = (None,) * len(new_schedule._fields)
        for emp in data.rownames:
            emp_schedule = new_schedule(f_name=data[emp, 'First'],
                                        l_name=data[emp, 'Last'],
                                        Monday=data[emp, 'Monday'],
                                        Tuesday=data[emp, 'Tuesday'],
                                        Wednesday=data[emp, 'Wednesday'],
                                        Thursday=data[emp, 'Thursday'],
                                        Friday=data[emp, 'Friday'],
                                        Saturday=data[emp, 'Saturday'],
                                        Sunday=data[emp, 'Sunday'])
            return_dict[emp] = emp_schedule
        return return_dict


