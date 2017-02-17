from os.path import dirname, abspath


class ReportTemplate(object):

    def __init__(self):
        self.path = dirname(dirname(abspath(__file__)))
        self.src_files = {}
        self._inr = None

    @property
    def interval(self):
        return self._inr

    def manual_input(self):
        pass

    def load(self):
        pass

    def run(self):
        pass

