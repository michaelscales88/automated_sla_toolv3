from PyQt5.QtCore import QThread, pyqtSignal


class ProgressBarWorker(QThread):
    update_progress = pyqtSignal(float, name='update_progress')

    def __init__(self, parent, proc):
        super().__init__(parent)
        self.proc = proc
        self.proc.finished_signal.connect(
            lambda: self.update_progress.emit(self.total))
        self.progress = 0
        self.buffer = 0
        self.total = 12056

    def run(self):
        while (self.progress <= self.total) and self.proc.qprocess.pid() is not None:
            if self.progress <= self.buffer:
                self.progress += self.buffer * .01
            self.update_progress.emit(self.progress)
            # time.sleep(0.2)

    def accumulate_std_out(self, std_out):
        self.buffer += len(std_out)