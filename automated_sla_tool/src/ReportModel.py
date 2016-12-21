from datetime import datetime as dt, timedelta as td
from dateutil.relativedelta import relativedelta as rd


class ReportTask(dict):
    def __init__(self, date=0):
        super().__init__()
        self._name = date
        self._data = {'target': None,
                      'data': None,
                      'started': False,
                      'completed': False
                      }

    @property
    def target(self):
        return self._data['target']

    @target.setter
    def target(self, new_target):
        self._data['target'] = new_target

    @property
    def day(self):
        return self._name

    @property
    def running(self):
        return self._data['started']

    @running.setter
    def running(self, value):
        self._data['started'] = value

    @property
    def complete(self):
        return self._data['completed']

    @property
    def data(self):
        return self._data['data']

    @data.setter
    def data(self, data):
        self._data['data'] = data
        self._data['completed'] = True

    @property
    def ready(self):
        return (True, False)[any((self._data['started'], self._data['completed']))]

    def __repr__(self):
        return ("Task name: {0}:\n"
                "Status: {1}\n"
                "Completed: {2}\n"
                "Data: {3}\n".format(self.day, self.running, self.complete, self._data['data']))

    def __getitem__(self, item):
        return self._data[item]


class ReportModel(object):
    def __init__(self, month, year=2016):
        self._model = {}
        self.init_model(month, year)

    @property
    def active(self):
        return False in [i.running for i in self._model.values()]

    def init_model(self, month, year):
        first_day = dt.strptime(month, '%B').date().replace(year=year)
        end_date = first_day + rd(months=1)
        today = dt.now().date()
        end_date = today if end_date > today else end_date
        while first_day < end_date:
            self._model[first_day] = ReportTask(first_day)
            first_day += td(days=1)

    def __getitem__(self, item):
        return self._model[item]

    def __repr__(self):
        return '\n'.join(['{}'.format(self._model[k]) for k in sorted(self._model.keys())])

    def get_next(self):
        for k, v in self._model.items():
            if self[k].ready is True:
                return self[k]
