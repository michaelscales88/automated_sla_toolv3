class ReportWorker(object):  # or threadworker
    def __init__(self):
        super().__init__()
        self._curr_rpt = None
        self._rpt_manifest = None

    @property
    def curr_rpt(self):
        return self._curr_rpt

    @curr_rpt.setter
    def curr_rpt(self, rpt_obj):
        self._curr_rpt = rpt_obj
        try:
            manifest = self._curr_rpt.manifest
        except AttributeError:
            self._curr_rpt = None
        else:
            self._rpt_manifest = manifest
