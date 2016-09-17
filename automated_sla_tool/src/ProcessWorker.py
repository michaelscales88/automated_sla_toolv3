import pyexcel as pe
from datetime import timedelta
from PyQt5.QtCore import QThread, pyqtSignal


class ProcessWorker(QThread):
    transmit_report = pyqtSignal(pe.sheets.sheet.Sheet, name='sheet')

    def __init__(self, proc=None, date_range=None):
        super().__init__()
        self.proc = proc
        self.dates = self.validate_dates(date_range)

    def __del__(self):
        self.wait()

    def validate_dates(self, date_range):
        if None in date_range:
            if date_range[0] is not None:
                date_range[1] = date_range[0]
            else:
                date_range[0] = date_range[1]
        else:
            pass
        return date_range

    def run(self):
        start_date = self.dates[0]
        end_date = self.dates[1]
        while start_date <= end_date:
            report = self.proc.main(start_date)
            self.transmit_report.emit(report)
            start_date += timedelta(days=1)
