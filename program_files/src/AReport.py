# Inherited report methods
import pyexcel as pe
import os


class AReport:
    def __init__(self, report_dates=None):
        self.path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if report_dates is None:
            raise ValueError('No report date provided... Try again.')
        self.dates = report_dates
        self.final_report = pe.Sheet()

    def get_sec(self, time_string):
        try:
            h, m, s = [int(float(i)) for i in time_string.split(':')]
        except TypeError:
            return 0
        return self.convert_sec(h, m, s)

    def convert_sec(self, h, m, s):
        return (3600 * int(h)) + (60 * int(m)) + int(s)

    def convert_time_stamp(self, convert_seconds):
        minutes, seconds = divmod(convert_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{0}:{1:02d}:{2:02d}".format(hours, minutes, seconds)

    def prepare_sheet_header(self, lst, first_index):
        return_list = [i for i in lst]
        return_list.insert(0, first_index)
        return [return_list]

    def transmit_report(self):
        return self.final_report
