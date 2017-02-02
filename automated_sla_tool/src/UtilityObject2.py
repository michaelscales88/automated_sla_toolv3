import os
import pyexcel as pe


class UtilityObject(object):

    @staticmethod
    def str_to_bool(bool_str):
        if type(bool_str) is bool:
            return bool_str
        elif bool_str in ('True', 'TRUE', 'true'):
            return True
        elif bool_str in ('False', 'false', 'FALSE'):
            return False
        else:
            raise ValueError("Cannot covert {} to a bool".format(bool_str))

    @staticmethod
    def get_sec(time_string):
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
        return UtilityObject.convert_sec(h, m, s)

    @staticmethod
    def convert_sec(h, m, s):
        return (3600 * int(h)) + (60 * int(m)) + int(s)

    @staticmethod
    def convert_time_stamp(convert_seconds):
        minutes, seconds = divmod(convert_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return r"{0}:{1:02d}:{2:02d}".format(hours, minutes, seconds)

    @staticmethod
    def change_dir(the_dir):
        try:
            os.chdir(the_dir)
        except FileNotFoundError:
            try:
                os.makedirs(the_dir, exist_ok=True)
                os.chdir(the_dir)
            except OSError:
                pass

    @staticmethod
    def load_data(file):
        if type(file) is pe.sheets.sheet.Sheet:
            return_file = file
        else:
            return_file = UtilityObject.open_pe_file(file)
        return_file.name_columns_by_row(0)
        return_file.name_rows_by_column(0)
        return return_file

    @staticmethod
    def open_pe_file(file):
        try:
            return_file = pe.get_sheet(file_name=file)
        except OSError:
            print('OSError ->'
                  'cannot open {}'.format(file))
        else:
            return return_file
