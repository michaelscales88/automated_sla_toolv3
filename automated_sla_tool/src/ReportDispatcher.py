import multiprocessing as mp
import logging
import traceback
from automated_sla_tool.src.FinishedDecorator import FinishedDecorator as check_running


class ReportDispatcher(object):

    running = False

    @check_running(running)
    def __init__(self, pool_size=3):
        super().__init__()
        self._max_size = pool_size
        self._pool = mp.Pool(processes=self._max_size)
        ReportDispatcher.running = True

    def ready_next(self):
        return self._pool._processes <= 3

    def start_task(self, target=None, output=None, **kwargs):
        # t = mp.Process(name='{}'.format(output.name), target=target, args=(kwargs.get('day'), output.data))
        # self._pool.append(t)
        # t.start()
        try:
            output.running = True
            output.data = self._pool.map(target, (kwargs.get('day'),))
        except Exception as e:
            print('Could not complete report dispatch '
                  'report date: {0}\nerr: {1}'.format(output.name, e))
            output.data = e


