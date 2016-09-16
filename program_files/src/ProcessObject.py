from collections import namedtuple
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtCore import QObject
from .ProcessButtonsWidget import ProcessButtonsWidget as PbWidget
from .TextWindowWidget import TextWindowWidget as TextOut
from .SaveWidget import SaveWidget
from .ExcelTabContainer import ExcelTabContainer as TabContainer
from .MyCalendarWidget import MyCalendarWidget as CalWidget


class ProcessObject(QObject):
    def __init__(self, parent=None, process=None):
        super().__init__(parent)
        self.__process_info = {
            'sla_report.py': ['download_documents()', 'load_documents()', 'compile_call_details()',
                              'scrutinize_abandon_group()', 'extract_report_information()', 'process_report()',
                              'save_report()'],
            'sla_slicer.py': []
        }
        try:
            proc_args = self.__process_info[process]
        except KeyError:
            raise TypeError('Tried to create process info: Failed'
                            'ProcessObject -> process info does not exist')
        else:
            self.date1 = None
            self.date2 = None
            Node = namedtuple('Node', 'name args buttons progress text_out, err_out file_saver cal1 cal2')
            Node.__new__.__defaults__ = (None,) * len(Node._fields)
            self.sub_proc = Node(name=process,
                                 args=proc_args,
                                 buttons=self.init_btns(proc_args),
                                 progress=self.init_prgrs(),
                                 text_out=self.init_txt(),
                                 err_out=self.init_err(),
                                 file_saver=self.init_save_widget(),
                                 cal1=CalWidget(name='Calendar 1'),
                                 cal2=CalWidget(name='Calendar 2'))
            self.data = self.init_data()
            self.sub_proc.cal1.updated_date.connect(self.update_date1)
            self.sub_proc.cal2.updated_date.connect(self.update_date2)

    def get_name(self):
        return self.sub_proc.name

    def update_date1(self, new_date):
        self.date1 = new_date

    def update_date2(self, new_date):
        self.date2 = new_date

    def init_data(self):
        return TabContainer(title='Spreadsheet Container')

    def init_save_widget(self):
        return SaveWidget()

    def init_btns(self, proc_args):
        return PbWidget(args=proc_args)

    def init_prgrs(self):
        return QProgressBar()

    def init_err(self):
        return TextOut(title='Error Log')

    def init_txt(self):
        return TextOut(title='Text Log')

    def get_ui(self):
        return self.sub_proc.buttons

    def get_progress_bar(self):
        return self.sub_proc.progress

    def get_err(self):
        return self.sub_proc.err_out

    def get_txt(self):
        return self.sub_proc.text_out

    def get_save_widget(self):
        return self.sub_proc.file_saver

    def get_data_widget(self):
        return self.data

    def get_cal_one(self):
        return self.sub_proc.cal1

    def get_cal_two(self):
        return self.sub_proc.cal2

    def get_date_one(self):
        return self.date1

    def get_date_two(self):
        return self.date2

    def add_data(self, data):
        self.sub_proc.file_saver.add_event(data.name)
        self.data.append_spreadsheet(data, data.name)
