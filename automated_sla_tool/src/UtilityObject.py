import os
import pyexcel as pe


class UtilityObject(object):
    def __init__(self):
        super().__init__()

    '''
    Primitive Utilities
    '''
    def str_to_bool(self, bool_str):
        if type(bool_str) is bool:
            return bool_str
        elif bool_str in ('True', 'TRUE', 'true'):
            return True
        elif bool_str in ('False', 'false', 'FALSE'):
            return False
        else:
            raise ValueError("Cannot covert {} to a bool".format(bool_str))

    def get_sec(self, time_string):
        try:
            h, m, s = [int(float(i)) for i in time_string.split(':')]
        except TypeError:
            return 0
        except ValueError:
            try:
                h, m = [int(float(i)) for i in time_string.split(':')]
                s = 0
            except ValueError:
                return 0
        return self.convert_sec(h, m, s)

    def convert_sec(self, h, m, s):
        return (3600 * int(h)) + (60 * int(m)) + int(s)

    def convert_time_stamp(self, convert_seconds):
        minutes, seconds = divmod(convert_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return r"{0}:{1:02d}:{2:02d}".format(hours, minutes, seconds)

    def change_dir(self, the_dir):
        try:
            os.chdir(the_dir)
        except FileNotFoundError:
            try:
                os.makedirs(the_dir, exist_ok=True)
                os.chdir(the_dir)
            except OSError:
                pass

    def load_data(self, file):
        if type(file) is pe.sheets.sheet.Sheet:
            return_file = file
        else:
            return_file = self.open_pe_file(file)
        return_file.name_columns_by_row(0)
        return_file.name_rows_by_column(0)
        return return_file

    def open_pe_file(self, file):
        try:
            return_file = pe.get_sheet(file_name=file)
        except OSError:
            print('OSError ->'
                  'cannot open {}'.format(file))
        else:
            return return_file