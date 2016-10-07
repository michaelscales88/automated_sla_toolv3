import os
import pyexcel as pe
from dateutil.parser import parse
from automated_sla_tool.src.AReport import AReport


class MarsReport(AReport):
    def __init__(self, month=None):
        super().__init__(report_dates=month)
        self.finished, report = self.report_finished()
        self.agent_time_card = None

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
        for sheet in self.agent_time_card:
            print(sheet)
            min_time = min([parse(date) for date in sheet.column['Logged In']])
            max_time = max([parse(date) for date in sheet.column['Logged Out']])
            # duration = sum([self.get_sec(time) for time in sheet.column['Duration']])
            print(min_time)
            print(max_time)
            # print(self.convert_time_stamp(duration))



    def process_report(self):
        pass

    def save_report(self):
        pass

    '''
    Utilities Section
    '''

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