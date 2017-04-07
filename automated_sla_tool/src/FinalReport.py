from os import startfile, makedirs
from os.path import dirname, join, basename
from datetime import date
from pyexcel import Sheet, get_sheet


class FinalReport(Sheet):
    def __init__(self, **kwargs):
        self._data = {
            'type': kwargs.get('report_type', None),
            'date': kwargs.get('report_date', None),
            'my_report': kwargs.get('my_report', None),
        }
        report_name = (
            self._data['date'].strftime("%m-%d-%Y") if isinstance(self._data['date'], date) else self._data['date']
        )
        super().__init__(name=report_name)
        self._finished = False
        self._table_set = False

    '''
    Properties
    '''

    @property
    def save_path(self):
        return r'{dir}\Output\{sub_dir}'.format(dir=dirname(self.report.path),
                                                sub_dir=self.type)

    @property
    def rpt_name(self):
        return '{d}_{t}'.format(d=self._data['date'].strftime("%m%d%Y"),
                                t=self._data['type'])

    @property
    def report(self):
        return self._data['my_report']

    @property
    def finished(self):
        return self._finished

    @finished.setter
    def finished(self, is_fin):
        self._finished = is_fin

    @property
    def type(self):
        return self._data['type']

    @property
    def date(self):
        return self._data['date']

    '''
    OS Operations
    '''

    def open_existing(self, the_file):
        if not self.finished:
            sheet = get_sheet(file_name=the_file)
            for row in sheet.rows():
                self.row += row
            self.name_columns_by_row(0)
            self.name_rows_by_column(0)
            self._finished = True

    # def resolve_name(self, str_fmt=None, f_ext='xlsx'):
    #     if str_fmt:
    #         file_string = str_fmt.format(date=self.date.strftime("%m%d%Y"))
    #     else:
    #         file_string = '{date}_{type}'.format(date=self.date, type=self.type)
    #     return '{f_string}.{fmt}'.format(f_string=file_string,
    #                                      fmt=f_ext)
    #
    # def resolve_path(self, tgt_path=None, sub_dir=None):
    #     try:
    #         if sub_dir:
    #             sub_dir = sub_dir.format(mo=self.date.strftime('%B'),
    #                                      yr=self.date.strftime('%Y'))
    #
    #         if tgt_path and sub_dir:
    #             path = join(tgt_path, sub_dir)
    #         elif sub_dir:
    #             path = join(self.save_path, sub_dir)
    #         else:
    #             raise ValueError()
    #     except ValueError:
    #         print('No location provided'
    #               'to save file: {name} {type}'.format(name=self.date,
    #                                                    type=self.type))
    #     else:
    #         return path

    # def save(self, str_fmt=None, save_fmt='xlsx', tgt_path=None, sub_dir=None, full_path=None):
    #     if full_path:
    #         folder_path = dirname(full_path)
    #         file_path = full_path
    #     else:
    #         folder_path = self.resolve_path(tgt_path=tgt_path,
    #                                         sub_dir=sub_dir)
    #         file_name = self.resolve_name(str_fmt=str_fmt,
    #                                       f_ext=save_fmt)
    #         file_path = join(folder_path, file_name)
    #     try:
    #         self.save_as(filename=file_path)
    #     except FileNotFoundError:
    #         makedirs(folder_path, exist_ok=True)
    #         self.save_as(filename=file_path)

    # def open(self, str_fmt=None, f_ext='xlsx', tgt_path=None, sub_dir=None, full_path=None):
    #     if full_path:
    #         startfile(full_path)
    #     else:
    #         folder_path = self.resolve_path(tgt_path=tgt_path,
    #                                         sub_dir=sub_dir)
    #         file_name = self.resolve_name(str_fmt=str_fmt,
    #                                       f_ext=f_ext)
    #         file_path = join(folder_path, file_name)
    #         startfile(file_path)

    '''
    Report Section
    '''

    def format_columns_with(self, f, *columns):  # w/ named rows and columns
        for column in columns:
            for col_name in self.colnames:
                if column in col_name:
                    for row_name in self.rownames:
                        self[row_name, col_name] = f(self[row_name, col_name])

    def make_programatic_column_with(self, f, column):
        # TODO could add colname and add values directly to final report **mind not handle issues well**
        new_rows = Sheet()
        new_rows.row += [column]
        # self.colnames += column
        for row in self.rows():
            row_w_headers = dict(zip(self.colnames, row))
            new_rows.row += f(row_w_headers)
        self.column += new_rows

    def __setitem__(self, key, value):
        try:
            super().__setitem__((self.rownames.index(key[0]), self.colnames.index(key[1])), value)
        except AttributeError:
            print('attriberror set_key')
