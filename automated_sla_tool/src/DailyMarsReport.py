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
        # TODO: add xslx writer for spreadsheet formatting
        super().__init__(report_dates=month)
        self.finished, report = self.check_finished()
        if self.finished:
            self.final_report = report
        else:
            (self.agent_time_card,
             self.agent_feature_trace) = self.load_documents()
            spreadsheet = r'M:\Help Desk\Schedules for OPS.xlsx'
            self.tracker = EmployeeTracker(spreadsheet, self.get_data_measurements())
            self.notes = Notes()

    '''
    UI Section
    '''

    def run(self):
        if self.finished:
            return
        else:
            agents = self.tracker.get_tracker()
            self.final_report = self.make_summary(self.tracker.get_header())
            for (ext, agent) in agents.items():
                if agent[self.day_of_wk]:
                    sheet_name = r'{0} {1}({2})'.format(agent.f_name, agent.l_name, ext)
                    try:
                        time_card = self.agent_time_card[sheet_name]
                        feature_card = self.agent_feature_trace[sheet_name]
                    except KeyError:
                        agent.data['Absent'] = 1
                    else:
                        try:
                            self.read_timecard(time_card, agent)
                        except IndexError:
                            # TODO improve this for catching Sun-Mon overnight employees
                            print('catching kristy on monday')
                            pass
                        self.read_featurecard(feature_card, agent)
                    finally:
                        self.final_report.row += self.tracker[ext]
            notes = [self.notes.pop(0)]
            self.final_report.row += notes
            self.final_report.row += self.notes.get_notes()
            self.final_report.name_rows_by_column(0)

    def save_report(self):
        self.set_save_path('mars_report')
        the_file = r'{0}_mars_report'.format(self.dates.strftime('%m%d%Y'))
        self.final_report.name = the_file
        file_string = r'.\{0}.xlsx'.format(the_file)
        self.final_report.save_as(filename=file_string)

    '''
    Utilities Section
    '''

    def check_day_card(self, time_card, shift_start, shift_end):
        prev_day = self.dates - timedelta(days=1)
        self.remove_row_w_day(time_card, prev_day)
        start_time = self.get_start_time(time_card.column['Logged In'])
        end_time = self.get_end_time(time_card.column['Logged Out'])
        clocked_in = start_time >= time(hour=1)
        clocked_out = end_time <= time(hour=23)
        # TODO improve this... checking for agents who didn't clock out and are late
        if not clocked_in and time_card.number_of_rows() is 2:
            start_time = self.get_start_time(time_card.column['Logged In'], overnight=True)
            clocked_in = True
        return (start_time if clocked_in else shift_start,
                end_time if clocked_out else shift_end,
                clocked_in,
                clocked_out)

    def check_night_card(self, time_card, shift_start, shift_end):
        tomorrow = self.dates + timedelta(days=1)
        self.remove_row_w_day(time_card, tomorrow)
        start_time = self.get_start_time(time_card.column['Logged In'], overnight=True)
        end_time = self.get_end_time(time_card.column['Logged Out'])
        clocked_in = start_time >= time(hour=1)
        clocked_out = end_time <= time(hour=23)
        return (start_time if clocked_in else shift_start,
                end_time if clocked_out else shift_end,
                clocked_in,
                clocked_out)

    def remove_row_w_day(self, time_card, remove_date):
        try:
            for r_index, event in enumerate(time_card.rows()):
                for index in event:
                    if self.safe_parse(index).date() == remove_date:
                        del time_card.row[r_index]
        except TypeError:
            print('Bad type: remove_date object'
                  '-> DailyMarsReport.remove_row_w_day')

    def query_sql_server(self):
        pass

    def load_documents(self):
        if self.finished:
            return
        else:
            agent_time_card_file = r'{0}\{1}'.format(self.src_doc_path, r'Agent Time Card.xlsx')
            agent_feature_trace_file = r'{0}\{1}'.format(self.src_doc_path, r'Agent Realtime Feature Trace.xlsx')
            try:
                agent_time_card = pe.get_book(file_name=agent_time_card_file)
                agent_feature_trace = pe.get_book(file_name=agent_feature_trace_file)
            except FileNotFoundError:
                self.download_documents(files=[r'Agent Time Card.xlsx', r'Agent Realtime Feature Trace.xlsx'])
                agent_time_card = pe.get_book(file_name=agent_time_card_file)
                agent_feature_trace = pe.get_book(file_name=agent_feature_trace_file)
            return self.filter_feature_report(agent_time_card), self.filter_feature_report(agent_feature_trace)

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
        if self.is_empty_wb(self.agent_time_card):
            raise OSError('No agents for report')
        return self.agent_time_card[0].colnames

    def read_featurecard(self, feature_card, emp_data):
        dnd_sec = self.correlate_list_data(feature_card.column['Feature Type'],
                                           feature_card.column['Duration'],
                                           'Do Not Disturb')
        emp_data.data['Availability'] = self.get_percent_avail(emp_data.data['Duration'], dnd_sec)
        emp_data.data['DND'] = self.convert_time_stamp(dnd_sec)

    def get_percent_avail(self, dt_time, div_sec):
        dt_delta = timedelta(hours=dt_time.hour, minutes=dt_time.minute, seconds=dt_time.second)
        dnd_delta = timedelta(seconds=div_sec)
        dt_delta = dnd_delta if dnd_delta > dt_delta else dt_delta
        return float(r'{0:.2f}'.format(((dt_delta - dnd_delta) / dt_delta) * 100))

    def read_timecard(self, time_card, emp_data):
        shift_start = emp_data[self.day_of_wk].start
        shift_end = emp_data[self.day_of_wk].end
        is_normal_shift = time(hour=0) <= shift_start <= time(hour=18, minute=59)

        if is_normal_shift:
            (emp_data.data['Logged In'],
             emp_data.data['Logged Out'],
             clocked_in,
             clocked_out) = self.check_day_card(time_card, shift_start, shift_end)
        else:
            (emp_data.data['Logged In'],
             emp_data.data['Logged Out'],
             clocked_in,
             clocked_out) = self.check_night_card(time_card, shift_start, shift_end)
            if clocked_in:
                emp_data.data.add_note(self.notes.add_time_note(r'Logged in {}'.format(
                    self.dates - timedelta(days=1)))
                )
        # TODO: this needs to calculate off real time in/out
        if clocked_in is False:
            emp_data.data.add_note(self.notes.add_time_note(r'No Login'))
        if clocked_out is False:
            emp_data.data.add_note(self.notes.add_time_note(r'No Logout'))
        try:
            duration = (datetime.min +
                        (datetime.combine(self.dates, emp_data.data['Logged Out']) -
                         datetime.combine(self.dates, emp_data.data['Logged In']))).time()
        except OverflowError:
            duration = (datetime.min +
                        (datetime.combine(self.dates + timedelta(days=1), emp_data.data['Logged Out']) -
                         datetime.combine(self.dates, emp_data.data['Logged In']))).time()
        emp_data.data['Duration'] = duration
        late = self.read_time(emp_data.data['Logged In']) > self.check_grace_pd(shift_start,
                                                                                minutes=timedelta(minutes=5))
        if clocked_in and late:
            emp_data.data['Late'] = 1

    def get_start_time(self, column, overnight=False):
        try:
            if overnight:
                return_time = max(self.safe_parse(item).time() for item in column)
            else:
                return_time = min(self.safe_parse(item).time() for item in column)
        except AttributeError:
            return_time = 'No Clock In'
        return return_time

    def get_end_time(self, column):
        try:
            return_time = max(self.safe_parse(item).time() for item in column)
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

    def filter_feature_report(self, workbook):
        try:
            del workbook['Summary']
        except KeyError:
            pass
        feature_report_filter = pe.RowValueFilter(self.feature_report_row_filter)
        for sheet in workbook:
            sheet.filter(feature_report_filter)
            sheet.name_columns_by_row(0)
            sheet.name_rows_by_column(0)
        return workbook

    def feature_report_row_filter(self, row):
        unique_cell = row[0].split(' ')
        return unique_cell[0] != 'Feature'

    def todays_date_row_filter(self, row):
        # TODO: Simplify... this seems overly complicated...
        dates = [self.safe_parse(dt_time=cell, default_rtn=self.util_datetime).date() for cell in row]
        return False in [(self.dates == date) for date in dates]

    def check_grace_pd(self, dt_t, minutes):
        return self.add_time(dt_t, add_time=minutes)

    def check_finished(self):
        the_file = r'{0}_mars_report.xlsx'.format(self.dates.strftime("%m%d%Y"))
        return super().report_finished('mars_report', the_file)


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
                                        data=EmployeeData(report_data))
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

    def __delitem__(self, ext):
        del self.__data[ext]

    def __getitem__(self, ext):
        agent_data = self.__data[ext]
        row_name = r'{0} {1}({2})'.format(agent_data.f_name, agent_data.l_name, ext)
        return [row_name] + agent_data.data.get_row()

    def get_tracker(self):
        return self.__data

    def get_header(self):
        return ['Employee'] + sorted(next(iter(self.__data.values())).data.keys())


class EmployeeData(object):
    def __init__(self, k_list):
        self.__dict = {}
        for key in k_list:
            self.__dict[key] = 0
        self.__dict['Absent'] = 0
        self.__dict['Late'] = 0
        self.__dict['DND'] = 0
        self.__dict['Availability'] = 0
        self.__dict['Notes'] = ''

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

    def add_note(self, note):
        self.__dict['Notes'] += r'{} '.format(note)

    def get_row(self):
        return [self.__dict[k] for k in sorted(self.__dict.keys())]

    def keys(self):
        return self.__dict.keys()
