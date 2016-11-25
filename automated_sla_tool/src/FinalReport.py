import pyexcel as pe
from copy import deepcopy as copy


class FinalReport(pe.Sheet):
    def __init__(self, report_type, report_date):
        super().__init__()
        self._finished = False
        self._type = report_type
        self._date = report_date
        self.name = '{0}_{1}'.format(self.date.strftime('%m%d%Y'), self.type)

    @property
    def finished(self):
        return self._finished

    @property
    def type(self):
        return self._type

    @property
    def date(self):
        return self._date

    def open_report(self, the_file):
        if not self.finished:
            sheet = pe.get_sheet(file_name=the_file)
            self.name = sheet.name
            for row in sheet.rows():
                self.row += row
            self.name_columns_by_row(0)
            self._finished = True

    def set_header(self, header):
        if not self.finished:
            self.row += header
            self.name_columns_by_row(0)

    def save_report(self, user_string=None, save_format='xlsx'):
        file_string = r'.\{0}_{1}.{2}'.format(self.date.strftime('%m%d%Y'),
                                              self.type,
                                              save_format) if user_string is None else user_string
        self.save_as(filename=file_string)

    def query_format(self):
        return copy(self).to_records()
