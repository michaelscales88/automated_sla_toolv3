import os
from datetime import datetime, time
from dateutil.parser import parse


class UtilityObject:
    def __init__(self, report_dates):
        if report_dates is None:
            raise ValueError('No report date provided... Try again.')
        self.dates = report_dates
        self.util_datetime = datetime.combine(self.dates, time())

    def str_to_bool(self, bool_str):
        if type(bool_str) is bool:
            return bool_str
        elif bool_str in ('True', 'TRUE', 'true'):
            return True
        elif bool_str in ('False', 'false', 'FALSE'):
            return False
        else:
            raise ValueError("Cannot covert {} to a bool".format(bool_str))

    def change_dir(self, the_dir):
        try:
            os.chdir(the_dir)
        except FileNotFoundError:
            try:
                os.makedirs(the_dir, exist_ok=True)
                os.chdir(the_dir)
            except OSError:
                pass

    def safe_parse(self, date=None, default=None, default_rtn=None):
        try:
            return parse(date, default=(default if default is not None else self.util_datetime))
        except ValueError:
            return default_rtn if default_rtn is not None else self.util_datetime
