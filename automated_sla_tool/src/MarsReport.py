from queue import Queue
from time import sleep
from datetime import datetime
from automated_sla_tool.src.ReportDispatcher import ReportDispatcher
from automated_sla_tool.src.ReportModel import ReportModel
from automated_sla_tool.src.DailyMarsReport import DailyMarsReport
from automated_sla_tool.src.UnbufferedPrint import Unbuffered


class MarsReport(ReportDispatcher):
    def __init__(self, **kwargs):
        super().__init__()
        self._model = ReportModel(month=kwargs.get('month', 'November'))
        self._queue = Queue()
        import sys
        sys.stdout = Unbuffered(sys.stdout)

    def run(self):
        print('Starting to run...', flush=True)
        while self._model.active:
            next_task = self._model.get_next()
            next_task.target = DailyMarsReport
            next_task.running = True
            self.submit_job(next_task)
        self.dispatch()
        print('Successful run!', flush=True)

    def print_model(self):
        print(self._model)

    def queue_day(self):
        today = datetime.today().date()
        start = datetime.now().time()
        print('starting queue day {}'.format(start))
        for day in (8, 15, 16):
            selection = datetime.today().date().replace(day=day)
            next_task = self._model[selection]
            next_task.target = DailyMarsReport
            next_task.running = True
            self.submit_job(next_task)
        self.dispatch()
        end = datetime.now().time()
        print('ended queue day {}'.format(end))
        print('duration: {}'.format((datetime.min +
                                     (datetime.combine(today, end) -
                                      datetime.combine(today, start))).time()))

    def queue_test(self):
        today = datetime.today().date()
        start = datetime.now().time()
        print('starting start_task {}'.format(start))
        selection = datetime.today().date().replace(day=8)
        next_task = self._model[selection]
        next_task.target = DailyMarsReport
        next_task.running = True
        self.submit_job(next_task)
        self.dispatch()
        selection = datetime.today().date().replace(day=15)
        next_task = self._model[selection]
        next_task.target = DailyMarsReport
        next_task.running = True
        self.submit_job(next_task)
        self.dispatch()
        selection = datetime.today().date().replace(day=16)
        next_task = self._model[selection]
        next_task.target = DailyMarsReport
        next_task.running = True
        self.submit_job(next_task)
        self.dispatch()
        end = datetime.now().time()
        print('ended start_task {}'.format(end))
        print('duration: {}'.format((datetime.min +
                                     (datetime.combine(today, end) -
                                      datetime.combine(today, start))).time()))
        # run1 = {
        #     'target': self.task1,
        #     'task_name': '1',
        #     'x': 14,
        #     'sleep_time': 2
        # }
        # run2 = {
        #     'target': self.task1,
        #     'task_name': '2',
        #     'x': 20,
        #     'sleep_time': 2
        # }
        # run3 = {
        #     'target': self.task1,
        #     'task_name': '3',
        #     'x': 10,
        #     'sleep_time': 1
        # }
        # self.submit_job(run1)
        # self.submit_job(run2)
        # self.submit_job(run3)
        # print('starting start_task {}'.format(datetime.now().time()))
        # self.dispatch()
        # print('ending start_task {}'.format(datetime.now().time()))

        # print('starting non start_task {}'.format(datetime.now().time()))
        # self.task2(run1['x'], run1['task_name'], run1['sleep_time'])
        # self.task2(run2['x'], run2['task_name'], run2['sleep_time'])
        # self.task2(run3['x'], run3['task_name'], run3['sleep_time'])
        # print('ending non start_task {}'.format(datetime.now().time()))
        # self.start_task(target=self.task2)
        # self.start_task(target=self.task3)

    def task1(self, x=2, task_name=None, sleep_time=2):
        rtn_string = ''
        y = 1
        while y < x:
            string = 'task {0}: run {1}: time: {2}'.format(task_name, y, datetime.now().time())
            # print('print inside task: {}'.format(string), flush=True)
            rtn_string += str(string + '\n')
            sleep(sleep_time)
            y += 1
        return rtn_string

    def task2(self, x=2, task_name=None, sleep_time=2):
        rtn_string = ''
        y = 1
        while y < x:
            string = 'task {0}: run {1}: time: {2}'.format(task_name, y, datetime.now().time())
            # print('print inside task: {}'.format(string), flush=True)
            rtn_string += str(string + '\n')
            sleep(sleep_time)
            y += 1
        print(rtn_string)

        # def task2(self, x=4):
        #     rtn_string = ''
        #     while x > 0:
        #         string = 'task2 {}'.format(datetime.now().time())
        #         print(string)
        #         rtn_string += str(string + '\n')
        #         sleep(.5)
        #     return rtn_string
        #
        # def task3(self, x=3):
        #     rtn_string = ''
        #     while x > 0:
        #         string = 'task3 {}'.format(datetime.now().time())
        #         print(string)
        #         rtn_string += str(string + '\n')
        #         sleep(1)
        #     return rtn_string
