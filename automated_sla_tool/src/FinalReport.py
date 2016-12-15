import pyexcel as pe
import ntpath
from os.path import splitext
from copy import deepcopy as copy


# TODO this might be better as an object with a sheet ->
# TODO to handle name conflict with nominable Sheet and prop sheet
class FinalReport(pe.Sheet):
    def __init__(self, report_type, report_date):
        super().__init__()
        self._finished = False
        self._type = report_type
        self._date = report_date
        try:
            self.name = '{0}_{1}'.format(self._date.strftime('%m%d%Y'), self._type)
        except AttributeError:
            self.name = '{0}_{1}'.format(self._date, self._type)

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
        if not self.finished and self.my_business(the_file):
            sheet = pe.get_sheet(file_name=the_file)
            for row in sheet.rows():
                self.row += row
            self.name_columns_by_row(0)
            self._finished = True

    def my_business(self, raw_file_string):
        file_string, ext = splitext(self.path_leaf(raw_file_string))
        if file_string == self.name:
            my_business = True
        else:
            my_business = self.check_fstring(file_string)
        return my_business

    def check_fstring(self, f):
        return all(x in self._type.split('_') + [self._date.strftime('%m%d%Y')] for x in f.split('_'))

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

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

    def format_columns_with(self, f, *columns):
        for column in columns:
            col_indices = [i for i, x in enumerate(self.colnames) if column in x]
            for col_index in col_indices:
                for row_index, row_val in enumerate(self.column_at(col_index)):
                    self[row_index, col_index] = f(row_val)

    def make_programatic_column_with(self, f, column):
        # TODO could add colname and add values directly to final report **mind not handle issues well**
        new_rows = pe.Sheet()
        new_rows.row += [column]
        # self.colnames += column
        for row in self.rows():
            row_w_headers = dict(zip(self.colnames, row))
            new_rows.row += f(row_w_headers)
        self.column += new_rows
