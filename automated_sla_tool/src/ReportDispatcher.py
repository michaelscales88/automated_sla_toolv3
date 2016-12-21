from concurrent.futures import ThreadPoolExecutor, as_completed
from automated_sla_tool.src.FinishedDecorator import FinishedDecorator as check_running


class ReportDispatcher(object):
    running = False

    @check_running(running)
    def __init__(self, pool_size=5):
        super().__init__()
        self._max_size = pool_size
        self._jobs = {}
        self._inc_jobs = []
        self._in_proc = {}
        # self._pool = ThreadPoolExecutor(max_workers=self._max_size)
        # print('{0} {1}'.format(self._pool, id(self._pool)))
        ReportDispatcher.running = True

    def listener(self, jobs):
        for job in as_completed(jobs):
            task_name = self._jobs[job]
            self._in_proc[task_name].data = job.result()
            del self._jobs[job]
            self._in_proc.pop(task_name)

    def submit_job(self, inc_job):
        self._inc_jobs.append(inc_job)

    def dispatch(self):
        # this_pool = self._pool
        # print('{0} {1}'.format(this_pool, id(this_pool)))
        with ThreadPoolExecutor(max_workers=self._max_size) as executor:
            for next_job in reversed(self._inc_jobs):
                # fnc = next_job.get('target', None)
                # x = next_job.get('x', None)
                # name = next_job.get('task_name', None)
                # sleep_time = next_job.get('sleep_time', None)
                # job = executor.submit(fn=fnc,
                #                       x=x,
                #                       task_name=name,
                #                       sleep_time=sleep_time)
                job = executor.submit(fn=next_job.target,
                                      day=next_job.day)
                self._jobs[job] = next_job.day
                # self._inc_jobs.remove(next_job)
                self._in_proc[next_job.day] = self._inc_jobs.pop(-1)
            self.listener(self._jobs)

    def print_inproc(self):
        print(self._in_proc)
