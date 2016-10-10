import pyexcel as pe
from datetime import timedelta
from PyQt5.QtCore import QThread, pyqtSignal


class ProcessWorker(QThread):
    transmit_report = pyqtSignal(pe.sheets.sheet.Sheet, name='sheet')

    def __init__(self, proc=None):
        super().__init__()
        self.proc = proc
        self.dates = self.validate_dates([self.proc.get_date_one(),
                                          self.proc.get_date_two()])

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
        try:
            proc = self.proc.get_proc()
            reports = proc.main(self.dates)
        except SystemExit:
            print('Process closing...')
        except Exception as err:
            print('Error Encountered ->'
                  'Terminating Process')
            self.proc.sub_proc.err_out.append(str(err))
        else:
            for report in reports:
                self.transmit_report.emit(report)