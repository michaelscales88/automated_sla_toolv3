import pyexcel as pe
import ntpath
from os.path import splitext
from copy import deepcopy as copy


# TODO this might be better as an object with a sheet ->
# TODO to handle name conflict with nominable Sheet and prop sheet
class FinalReport(pe.Sheet):
    def __init__(self, **kwargs):
        self._data = {
            'type': kwargs.get('report_type', None),
            'date': kwargs.get('report_date', None),
            'rownames': kwargs.get('rownames', ()),
            'colnames': kwargs.get('colnames', ()),
        }
        super().__init__(name=self._data['date'].strftime("%m-%d-%Y"))
        self._finished = False
        self._table_set = False

    @property
    def rpt_name(self):
        return '{d}_{t}'.format(d=self._data['date'].strftime("%m%d%Y"),
                                t=self._data['type'])

    @property
    def finished(self):
        return self._finished

    @property
    def type(self):
        return self._data['type']

    @property
    def date(self):
        return self._data['date']

    @property
    def summary(self):
        rtn_list = ['Summary']
        for colname in self.colnames:
            try:
                fn = self._data['colnames'][colname]
                column = self.column[colname]
                rtn_val = fn(column)  # Try to call stored column fn
            except TypeError:
                instructions = self._data['colnames'][colname]
                fn = instructions.pop('fn', None)
                columns = {
                    k : self.column[v] for k, v in instructions.items()
                }
                rtn_val = fn(**columns)
            rtn_list.append(rtn_val)
        return rtn_list

    def set_header(self, header):
        if not self.finished:
            self._data['colnames'] = header
            if self.is_set('rownames'):
                self.init_table()

    def set_rows(self, rows):
        if not self.finished:
            self._data['rownames'] = rows
            self.init_table()

    def init_table(self):
        if not self._table_set and self.is_set('colnames') and self.is_set('rownames'):
            self.colnames += [''] + list(self._data['colnames'])
            for row in self._data['rownames']:
                self.row += [row] + [0 for x in range(len(self.colnames) - 1)]
            self.name_rows_by_column(0)
            self._table_set = True

    '''
    OS Operations
    '''

    def open_report(self, the_file):
        if not self.finished and self.my_business(the_file):
            sheet = pe.get_sheet(file_name=the_file)
            for row in sheet.rows():
                self.row += row
            self.name_columns_by_row(0)
            self._finished = True

    def my_business(self, raw_file_string):
        file_string, ext = splitext(self.path_leaf(raw_file_string))
        if file_string == self.rpt_name:
            my_business = True
        else:
            my_business = self.check_fstring(file_string)
        return my_business

    def check_fstring(self, f):
        return all(x in self._data['type'].split('_') + [self._data['date'].strftime('%m%d%Y')] for x in f.split('_'))

    def path_leaf(self, path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    def save_report(self, user_string=None, save_format='xlsx'):
        file_string = r'.\{0}_{1}.{2}'.format(self.date.strftime('%m%d%Y'),
                                              self.type,
                                              save_format) if user_string is None else user_string
        self.save_as(filename=file_string)

    '''
    Default Column Fnc
    '''

    def sum(self, col):
        return sum(col)

    def avg(self, col):
        numer = 0
        denom = 0
        for val in col:
            if val > 0:
                numer += val
                denom += 1
        return numer / denom

    '''
    Report Section
    '''

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

    def is_set(self, key):
        return self._data.get(key, None)

    def __setitem__(self, key, value):
        try:
            super().__setitem__((self.rownames.index(key[0]), self.colnames.index(key[1])), value)
        except AttributeError:
            print('attriberror setkey')